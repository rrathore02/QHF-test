import mcmodules
import types
import keyparams
import numpy as np

#===========[ Cyanobacteria ]======================
def Cyanobacteria_UAv1p0():
    global Module_Cyanobacteria
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Cyanobacteria AE v1.0')
    ModuleTemp.add_input('Temperature')
    ModuleTemp.add_input('Pressure')
    ModuleTemp.add_output('Suitability')
    def _execute(self):
        if keyparams.Pressure > 0.007 and keyparams.Temperature < 343. and keyparams.Temperature > 273.:
            keyparams.Suitability=1.0
        else:
            keyparams.Suitability=0.0
        print('Suitability calculated in module', keyparams.Suitability)
        # Key parameters are returned to the main function, allowing the Visualization
        # of the results. The parameters are passed on through a shared module (keyparams)
        keyparams.runid = keyparams.runid+' | '+ 'Cyanobacteria AE V1.0'

    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.activate()
    Module_Cyanobacteria = ModuleTemp
    return Module_Cyanobacteria
