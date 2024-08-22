import mcmodules
import math
import types
import numpy as np
import keyparams

#================================================
def marsmodules():
# Modules for simple Mars surface/subsurface model, one of the examples for the Quantitative Habitability Framework
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
        mu_albedo, sigma_albedo = 0.25, 0.04 # mean and standard deviation, https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html (std dev assumed to account for local surface albedo variations)
        keyparams.Bond_Albedo = np.random.normal(mu_albedo, sigma_albedo, 1)[0]

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
        keyparams.Semi_major_axis = 1.524 # sma in astronomical units
        keyparams.Orbital_Period = 686.980 # period in days, from Agol et al. 2021, Table 2
        keyparams.Eccentricity = 0.0935 # average eccentricity, not determined
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
    ModuleTemp.add_output('Mantle_Composition')
    #ModuleTemp.add_output('Volatile_Content')
    ModuleTemp.add_output('Depth')  # Parameter sampling the depth in meters - from 0. (surface) to 5,000
    ModuleTemp.add_output('Density')
    ModuleTemp.add_output('Gravity')
    def _execute(self):
        keyparams.runid = 'Mars AE v0.1'
        #global Planet_Mass_Mstar,  Mantle_Composition
        mu_p, sigma_p = 3.2260e-07, 0.00 # mean and standard deviation in Mstar, from https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
        keyparams.Planet_Mass_Mstar = np.random.normal(mu_p, sigma_p, 1)[0] # Planet mass in units of stellar mass
        Msol = 1.98910e30 # Solar mass in kilograms
        MEarth = 5.9736e24 # Earth mass in kilograms
        unitconversion = MEarth / Msol # Convert Solar mass to Earth mass
        keyparams.Planet_Mass = keyparams.Planet_Mass_Mstar * keyparams.Stellar_Mass * unitconversion # Planet mass in Earth masses
        #keyparams.Mantle_Composition = [0.7,0.3] # Fe / Si / Mg mass ratio
        keyparams.Gravity= 3.73 # m/s2 surface gravity
        keyparams.Density = 2582.00   # kg/m3  Density of the crust
        if keyparams.ProbeIndex is not None:        # Is the program sampling multiple locations in the parameter space?
            keyparams.Depth = keyparams.ProbeIndex * 1000. # If so, depth [in meter] is calculated from the probe index
        else:
            keyparams.Depth = np.random.uniform(low=0., high=5000.)[0] # Depth in meter
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
    ModuleTemp.add_output('Surface_Pressure')
    ModuleTemp.add_output('Internal_Pressure')
    def _execute(self):
        mu_p, sigma_p = 0.007, 0.002 # mean and standard deviation, pressure in units of atm
        keyparams.Surface_Pressure = np.random.normal(mu_p, sigma_p, 1)[0]
        keyparams.Surface_Pressure = np.clip(keyparams.Surface_Pressure, 0., 5e3) # Limit pressure to the range in which the lower T boundary of the water phase diagram is mostly constant
        keyparams.Internal_Pressure = keyparams.Surface_Pressure + (keyparams.Depth * keyparams.Gravity * keyparams.Density)/101325.  # Pressure at Depth equals atmospheric pressure plus density times gravity times column height (i.e., depth)
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
    def _execute(self):
        #global Equilibrium_Temp
        SBsigma = 5.670373e-8 # Stefan-Boltzmann sigma, in W/m^2/K^4
        au2m = 1.496e11 # au in meters
        Lsun = 3.939e26 # Solar luminosity in Watt
        keyparams.Equilibrium_Temp = ( (keyparams.Luminosity*Lsun)*(1-keyparams.Bond_Albedo) / (16 * np.pi *SBsigma * (keyparams.Semi_major_axis*au2m)**2))**(1/4)
        #keyparams.Surface_Temperature = ( (keyparams.Luminosity*Lsun)*(1-keyparams.Bond_Albedo) / (16 * np.pi *SBsigma * (keyparams.Semi_major_axis*au2m)**2))**(1/4)
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.activate()
    ModuleTemp.define_ID(m_id)
    ModuleEqTemperature = ModuleTemp
    m_id=m_id+1

#===============================================
    global ModuleGreenhouse
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Greenhouse \n Effect')
    ModuleTemp.add_input('Equilibrium_Temp')
    ModuleTemp.add_input('Planet_Mass')
    ModuleTemp.add_input('Mantle_Composition')
    #ModuleTemp.add_input('Volatile_Content')
    ModuleTemp.add_output('Surface_Temperature')
    def _execute(self):
        #global Surface_Temperature, GreenhouseWarming
        mu_gh, sigma_gh = 90., 15. # mean and standard deviation, in K, of Greenhouse effect
        keyparams.GreenhouseWarming = np.random.normal(mu_gh, sigma_gh, 1)[0]
        keyparams.Surface_Temperature = keyparams.GreenhouseWarming + keyparams.Equilibrium_Temp
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.visualize()
    ModuleTemp.activate()
    #ModuleGreenhouse = ModuleTemp
    m_id=m_id+1

#===============================================
    global ModuleLeakyGreenhouse
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Leaky Greenhouse')
    ModuleTemp.add_input('Equilibrium_Temp')
    ModuleTemp.add_input('Planet_Mass')
    ModuleTemp.add_input('Mantle_Composition')
    #ModuleTemp.add_input('Volatile_Content')
    ModuleTemp.add_output('Surface_Temperature')
    def _execute(self):
        #global Surface_Temperature, GreenhouseWarming
        mu_alpha, sigma_alpha = 0.1, 0.02 # mean and standard deviation of alpha, the key parameter of the single-layer leaky greenhouse model.
        alpha = np.random.normal(mu_alpha, sigma_alpha, 1)[0]
        alpha = np.clip(alpha, 0.,1.0)
        keyparams.GreenhouseWarming =  keyparams.Equilibrium_Temp * (2.0/(2.0-alpha))**(1/4.) - keyparams.Equilibrium_Temp
        keyparams.Surface_Temperature = keyparams.Equilibrium_Temp + keyparams.GreenhouseWarming
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.visualize()
    ModuleTemp.activate()
    ModuleGreenhouse = ModuleTemp
    m_id=m_id+1


#===============================================
    global ModuleInterior
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Interior \n Processes')
    ModuleTemp.add_input('Surface_Temperature')
    ModuleTemp.add_output('Temperature')
    def _execute(self):
        mu_tgrad, sigma_tgrad = 0.002, 0.0005 # mean and standard deviation, in K/m of the temperature gradient
        #keyparams.Thermal_Gradient = np.clip(np.random.normal(mu_tgrad, sigma_tgrad, 1), 0.0, 1000.) # Make sure Temperature gradient is not negative
        keyparams.Thermal_Gradient = np.random.normal(mu_tgrad, sigma_tgrad, 1)[0]
        keyparams.Interior_Temperature= keyparams.Surface_Temperature + keyparams.Depth * keyparams.Thermal_Gradient
        keyparams.Temperature = keyparams.Interior_Temperature
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.visualize()
    ModuleTemp.activate()
    ModuleInterior = ModuleTemp
    m_id=m_id+1

#===============================================

    return [ModuleStar, ModuleAlbedo, ModuleOrbit, ModulePressure, ModuleEqTemperature, ModuleGreenhouse,ModulePlanetPriors,ModuleInterior] #,ModuleHabitability,Cyanobacteria_UAv1p0]
    return [ModuleStar, ModuleAlbedo, ModuleOrbit, ModulePressure, ModuleEqTemperature, ModulePlanetPriors,ModuleInterior] #,ModuleHabitability,Cyanobacteria_UAv1p0]
