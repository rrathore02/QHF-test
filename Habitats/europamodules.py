import mcmodules
import math
import types
import numpy as np
import keyparams

#================================================
def europamodules():
# Modules for simple Europa surface/subsurface model, one of the examples for the Quantitative Habitability Framework
#
#
    m_id = 0
    global ModuleAlbedo
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Albedo Prior')
    ModuleTemp.add_output('Bond_Albedo')
    ModuleTemp.define_ID(m_id)
    m_id=m_id+1
    ModuleTemp.activate()
    def _execute(self):
        #global Bond_Albedo
        mu_albedo, sigma_albedo = 0.64, 0.00 # mean and standard deviation. The albedo is from "The Planetary Scientist's Companion", Lodders & Fegley
        # draw a random albedo from the distribution, limited between 0 and 1
        keyparams.Bond_Albedo = np.clip(np.random.normal(mu_albedo, sigma_albedo, 1)[0], a_min=0., a_max=1.)

    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleAlbedo = ModuleTemp

#===============================================
    global ModuleStar
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Stellar \n Properties')
    ModuleTemp.add_output('Luminosity') # in Msol
    ModuleTemp.add_output('Stellar_Mass') # in Msun
    ModuleTemp.add_output('Stellar_Age') # in Myr
    ModuleTemp.define_ID(m_id)
    ModuleTemp.activate()
    def _execute(self):
        #global Luminosity, Stellar_Mass, Stellar_Age
        keyparams.Luminosity = mu_st_lum, sigma_st_lum = 1.0, 0.00001 # Solar luminosity is 1.0 in Lsol units
        keyparams.Luminosity = np.random.normal(mu_st_lum, sigma_st_lum, 1)[0]
        mu_st_mass, sigma_st_mass = 1.0000, 0.000001 # mean and standard deviation, Solar mass in solar units
        keyparams.Stellar_Mass = np.random.normal(mu_st_mass, sigma_st_mass, 1)[0]
        keyparams.Stellar_Age = 4.567 # average eccentricity
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleStar = ModuleTemp
    m_id=m_id+1

#===============================================
    global Orbit
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Orbital \n Parameters')
    ModuleTemp.add_output('Orbital_Period')
    ModuleTemp.add_output('Semi_major_axis')
    ModuleTemp.add_output('Eccentricity')
    def _execute(self):
        #global Semi_major_axis, Orbital_Period, Eccentricity
        keyparams.Semi_major_axis = 5.20 # Jupiter's sma in astronomical units
        keyparams.Orbital_Period = 4331.980 # Jupiter's orbital period in days, from https://nssdc.gsfc.nasa.gov/planetary/factsheet/
        keyparams.Eccentricity = 0.0049 # Jupiter's average eccentricity, not determined
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.activate()
    ModuleOrbit = ModuleTemp
    m_id=m_id+1
#===============================================
    global ModulePlanetPriors
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Planet \n Primary Properties')
    ModuleTemp.add_input('Stellar_Mass')
    ModuleTemp.add_output('Planet_Mass')
    ModuleTemp.add_output('Depth')  # Parameter sampling the depth in meters - from 0. (surface) to 5,000
    ModuleTemp.add_output('Ice_Thickness')  # Parameter describing the thickness of Europa's ice layer
    ModuleTemp.add_output('Density')
    ModuleTemp.add_output('Gravity')
    def _execute(self):
        keyparams.runid = 'Europa AE v0.1'
        Msol = 1.98910e30 # Solar mass in kilograms
        MEarth = 5.9736e24 # Earth mass in kilograms
        mu_p, sigma_p = 0.47910e23 / Msol, 0.00 # mean and standard deviation in units of Mstar, from "The Planetary Scientist's Companion", Lodders & Fegley
        keyparams.Planet_Mass_Mstar = np.random.normal(mu_p, sigma_p, 1)[0] # Planet mass in units of stellar mass
        unitconversion = MEarth / Msol # Convert Solar mass to Earth mass
        keyparams.Planet_Mass = keyparams.Planet_Mass_Mstar * keyparams.Stellar_Mass * unitconversion # Planet mass in Earth masses
        #keyparams.Mantle_Composition = [0.7,0.3] # Fe / Si / Mg mass ratio
        keyparams.Gravity= 1.31 # m/s2 surface gravity
        keyparams.Density = 3018.00   # kg/m3  Bulk Density, from "The Planetary Scientist's Companion", Lodders & Fegley
        if keyparams.ProbeIndex is not None:        # Is the program sampling multiple locations in the parameter space?
            keyparams.Depth = keyparams.ProbeIndex * 1000. # If so, depth [in meter] is calculated from the probe index
        else:
            keyparams.Depth = np.random.uniform(low=0., high=128_000.)[0] # Depth in meter
        # make sure depth doesn't run below rocky interior:
        #    assumes rocky interior is at ~128,000 m depth
        if keyparams.Depth > 128_000:
            keyparams.Depth = 128_000#np.random.uniform(low=0., high=128_000.)

        mu_ice, sigma_ice = 20000., 4000. # mean and standard deviation in units of  # Ice thickness mean and 1 sigma, in meters; assumption
        keyparams.Mean_IceThickness  = mu_ice
        keyparams.Ice_Thickness = np.clip(np.random.normal(mu_ice, sigma_ice, 1),0.0, 20_000.).item() # Ice thickness
        #print(keyparams.Ice_Thickness.item())

    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.activate()
    ModulePlanetPriors = ModuleTemp
    m_id=m_id+1


#===============================================
    global ModulePressure
    global Surface_Pressure
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Surface \n Pressure Prior')
    ModuleTemp.add_input('Depth')
    ModuleTemp.add_input('Gravity')
    ModuleTemp.add_input('Density')
    #ModuleTemp.add_output('Surface_Pressure')
    ModuleTemp.add_output('Internal_Pressure')
    def _execute(self):
        mu_p, sigma_p = 0.000, 0.000 # mean and standard deviation, pressure in units of atm -- Lacking an atmosphere, Europa does not have atmospheric pressure
        keyparams.Surface_Pressure = np.random.normal(mu_p, sigma_p, 1)[0]
        keyparams.Surface_Pressure = np.clip(keyparams.Surface_Pressure, 0., 5e3) # Limit pressure to the range in which the lower T boundary of the water phase diagram is mostly constant
        keyparams.Internal_Pressure = keyparams.Surface_Pressure + (keyparams.Depth * keyparams.Gravity * keyparams.Density)/101325.  # Pressure at Depth equals atmospheric pressure plus density times gravity times column height (i.e., depth)
        # fix Internal_Pressure being single-valued array to being a float
        keyparams.Internal_Pressure = keyparams.Internal_Pressure
        keyparams.Pressure = keyparams.Internal_Pressure
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.activate()
    ModulePressure = ModuleTemp
    m_id=m_id+1



#===============================================
    global ModuleEqTemperature
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Equilibrium \n Temperature')
    ModuleTemp.add_input('Semi_major_axis')
    ModuleTemp.add_input('Bond_Albedo')
    ModuleTemp.add_input('Luminosity')
    ModuleTemp.add_output('Equilibrium_Temp')
    ModuleTemp.add_output('Surface_Temperature')
    def _execute(self):
        #global Equilibrium_Temp
        SBsigma = 5.670373e-8 # Stefan-Boltzmann sigma, in W/m^2/K^4
        au2m = 1.496e11 # au in meters
        Lsun = 3.939e26 # Solar luminosity in Watt
        keyparams.Equilibrium_Temp = ( (keyparams.Luminosity*Lsun)*(1-keyparams.Bond_Albedo) / (16 * np.pi *SBsigma * (keyparams.Semi_major_axis*au2m)**2))**(1/4)
        print(keyparams.Equilibrium_Temp)
        keyparams.Surface_Temperature = keyparams.Equilibrium_Temp # With no atmosphere, assume that these two are equal
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.activate()
    ModuleTemp.define_ID(m_id)
    ModuleEqTemperature = ModuleTemp
    m_id=m_id+1


#===============================================
    global ModuleInterior
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Interior \n Processes')
    ModuleTemp.add_input('Internal_Pressure')
    ModuleTemp.add_input('Surface_Temperature')
    ModuleTemp.add_output('Temperature')
    def _execute(self):
        #mu_tgrad_ice, sigma_tgrad_ice = 0.001, 0.00 # mean and standard deviation, in K/m of the temperature gradient in ice
        #keyparams.Thermal_Gradient_Ice = np.random.normal(mu_tgrad_ice, sigma_tgrad_ice, 1)[0]
        # set thermal gradient in ice based on linear function btwn surface and user-set boundary temp
        keyparams.WaterIceBoundary_Temperature = 273.15
        keyparams.Thermal_Gradient_Ice = (keyparams.WaterIceBoundary_Temperature - keyparams.Surface_Temperature) / keyparams.Ice_Thickness
        
        
        #print([keyparams.Depth,keyparams.Ice_Thickness])
        keyparams.Interior_Temperature= keyparams.Surface_Temperature + np.min([keyparams.Depth,keyparams.Ice_Thickness]) * keyparams.Thermal_Gradient_Ice

        #mu_tgrad_water, sigma_tgrad_water = 0.005, 0.001 # mean and standard deviation, in K/m of the temperature gradient in water ocean
        #keyparams.Thermal_Gradient_Water = np.random.normal(mu_tgrad_water, sigma_tgrad_water, 1)[0]
        
        # calculate the temperature at the very bottom of the ice layer
        # this will be the starting point for the water temperature profile
        #keyparams.Surface_Temperature + (keyparams.Ice_Thickness*keyparams.Thermal_Gradient_Ice)
        # calculate the ocean thermal profile following our quadratic parameterization of the Vance+ profiles:
        # T = a*x^2 + m*x + b; a,m are fitted coefficients; x = depth below water/ice boundary; b = temp at boundary
        a = 0.000000000148
        m = 0.00001102
        
        if keyparams.Depth <= keyparams.Ice_Thickness:
            # here, we're inside the ice:
            keyparams.Interior_Temperature = keyparams.Surface_Temperature + (keyparams.Depth*keyparams.Thermal_Gradient_Ice)
        elif keyparams.Depth > keyparams.Ice_Thickness:
            # here, we're inside the ocean
            relative_depth = abs(keyparams.Depth - keyparams.Ice_Thickness)
            keyparams.Interior_Temperature = (a*relative_depth**2) + (m*relative_depth) + keyparams.WaterIceBoundary_Temperature
        #keyparams.Interior_Temperature = keyparams.Interior_Temperature
        keyparams.Temperature = keyparams.Interior_Temperature
        # note the above will always be > the boundary temperature, so don't need to enforce a lower-T-limit boundary condition
        
#         # Calculate the water column above current depth (not the ice) and add the temperature difference:
#         if keyparams.Depth > keyparams.Ice_Thickness:
#             keyparams.Interior_Temperature += (keyparams.Depth - keyparams.Ice_Thickness) * keyparams.Thermal_Gradient_Water
#         # Interior_Temperature calculated as a single-value array so need to pull that single-value out before saving
#         keyparams.Interior_Temperature = keyparams.Interior_Temperature
#         keyparams.Temperature = keyparams.Interior_Temperature
        
#         # Enforce physical limits:
#         freezing_point = 273. # freezing point of water in [Kelvin]
#         if keyparams.Temperature < freezing_point:
#             keyparams.Temperature = freezing_point # the ocean temperature (at the surface of the ocean) can't be below the freezing point

    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.visualize()
    ModuleTemp.activate()
    ModuleInterior = ModuleTemp
    m_id=m_id+1

#===============================================


    return [ModuleStar, ModuleAlbedo, ModuleOrbit, ModulePressure, ModuleEqTemperature, ModulePlanetPriors,ModuleInterior] #,ModuleHabitability,Cyanobacteria_UAv1p0]
