import mcmodules
import math
import types
import numpy as np
import keyparams

#================================================
def TRAPPIST1fModules():
# https://exoplanetarchive.ipac.caltech.edu/overview/TRAPPIST-1e#planet_TRAPPIST-1-e_collapsible
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
        mu_albedo, sigma_albedo = 0.3, 0.13 # mean and standard deviation
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
        keyparams.Luminosity = mu_st_lum, sigma_st_lum = 0.000553, 1.92e-5 # mean and standard deviation, Agol et al. 2021 Planetary Science Journal, 2:1, Table 7
        keyparams.Luminosity = np.random.normal(mu_st_lum, sigma_st_lum, 1)
        mu_st_mass, sigma_st_mass = 0.0898, 0.0023 # mean and standard deviation, Mann et al. 2019
        keyparams.Stellar_Mass = np.random.normal(mu_st_mass, sigma_st_mass, 1)
        keyparams.Stellar_Age = 0.00 # average eccentricity
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
        keyparams.Semi_major_axis = 0.03849 # sma in astronomical units
        keyparams.Orbital_Period = 9.207540 # period in days, from Agol et al. 2021, Table 2
        keyparams.Eccentricity = 0.00 # average eccentricity, not determined
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.activate()
    ModuleOrbit = ModuleTemp
    m_id=m_id+1

#===============================================
    global ModulePressure
    global Surface_Pressure
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Surface \n Pressure Prior')
    ModuleTemp.add_output('Surface_Pressure')
    ModuleTemp.add_output('Pressure')
    def _execute(self):
        mu_p, sigma_p = 1.0, 0.5 # mean and standard deviation, pressure in units of atm
        keyparams.Surface_Pressure = np.random.normal(mu_p, sigma_p, 1)
        keyparams.Surface_Pressure = np.clip(keyparams.Surface_Pressure, 0., 5e3) # Limit pressure to the range in which the lower T boundary of the water phase diagram is mostly constant
        keyparams.Pressure = keyparams.Surface_Pressure
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.activate()
    ModulePressure = ModuleTemp
    m_id=m_id+1

#===============================================
    global ModulePlanetPriors
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Planet \n Primary Properties')
    ModuleTemp.add_input('Stellar_Mass')
    ModuleTemp.add_output('Planet_Mass')
    ModuleTemp.add_output('Mantle_Composition')
    ModuleTemp.add_output('Volatile_Content')
    def _execute(self):
        keyparams.runid = 'TRAPPIST-1f-like Planet v1.0'
        #global Planet_Mass_Mstar,  Mantle_Composition
        mu_p, sigma_p = 2.313e-5, 0.043e-5 # mean and standard deviation in Mstar, from Agol et al. 2021 Table 2
        keyparams.Planet_Mass_Mstar = np.random.normal(mu_p, sigma_p, 1) # Planet mass in units of stellar mass
        Msol = 1.98910e30 # Solar mass in kilograms
        MEarth = 5.9736e24 # Earth mass in kilograms
        unitconversion = MEarth / Msol # Convert Solar mass to Earth mass
        keyparams.Planet_Mass = keyparams.Planet_Mass_Mstar * keyparams.Stellar_Mass * unitconversion # Planet mass in Earth masses
        keyparams.Mantle_Composition = [0.7,0.3] # Fe / Si / Mg mass ratio
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.activate()
    ModulePlanetPriors = ModuleTemp
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
    #ModuleTemp.add_input('Mantle_Composition')
    #ModuleTemp.add_input('Volatile_Content')
    ModuleTemp.add_output('Surface_Temperature')
    ModuleTemp.add_output('Temperature')
    def _execute(self):
        mu_gh, sigma_gh = 90., 15. # mean and standard deviation, in K, of Greenhouse effect
        keyparams.GreenhouseWarming = np.random.normal(mu_gh, sigma_gh, 1)
        keyparams.Surface_Temperature = keyparams.GreenhouseWarming + keyparams.Equilibrium_Temp
        keyparams.Temperature = keyparams.Surface_Temperature
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.visualize()
    ModuleTemp.activate()
    ModuleGreenhouse = ModuleTemp
    m_id=m_id+1

#===============================================
    global ModuleLeakyGreenhouse
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Leaky Greenhouse')
    ModuleTemp.add_input('Equilibrium_Temp')
    ModuleTemp.add_input('Planet_Mass')
    #ModuleTemp.add_input('Mantle_Composition')
    #ModuleTemp.add_input('Volatile_Content')
    ModuleTemp.add_output('Surface_Temperature')
    ModuleTemp.add_output('Temperature')
    def _execute(self):
        mu_alpha, sigma_alpha = 0.95, 0.01 # mean and standard deviation of alpha, the key parameter of the single-layer leaky greenhouse model.
        alpha = np.random.normal(mu_alpha, sigma_alpha, 1)
        alpha = np.clip(alpha, 0.,1.0)
        keyparams.GreenhouseWarming =  keyparams.Equilibrium_Temp * (2.0/(2.0-alpha))**(1/4.) - keyparams.Equilibrium_Temp
        keyparams.Surface_Temperature = keyparams.Equilibrium_Temp + keyparams.GreenhouseWarming
        keyparams.Temperature = keyparams.Surface_Temperature
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.visualize()
    ModuleTemp.activate()
    #ModuleGreenhouse = ModuleTemp
    m_id=m_id+1


#===============================================
    global ModuleInterior
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Interior \n Processes')
    #ModuleTemp.add_input('Equilibrium_Temp')
    ModuleTemp.add_input('Planet_Mass')
    #ModuleTemp.add_input('Mantle_Composition')
    #ModuleTemp.add_input('Volatile_Content')
    ModuleTemp.add_output('Outgassing')
    ModuleTemp.add_output('Atm. Sinks')
    def _execute(self):
        mu_gh, sigma_gh = 110., 50. # mean and standard deviation, in K, of Greenhouse effect
        keyparams.GreenhouseWarming = np.random.normal(mu_gh, sigma_gh, 1)
        keyparams.Surface_Temperature = keyparams.GreenhouseWarming + keyparams.Equilibrium_Temp
        keyparams.Temperature = keyparams.Surface_Temperature
    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.define_ID(m_id)
    ModuleTemp.visualize()
    ModuleTemp.activate()
    ModuleInterior = ModuleTemp
    m_id=m_id+1

#===============================================
    return [ModuleStar, ModuleAlbedo, ModuleOrbit, ModulePressure, ModuleEqTemperature, ModuleGreenhouse,ModulePlanetPriors] #,ModuleHabitability,Cyanobacteria_UAv1p0]
