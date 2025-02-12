import mcmodules
import types
import keyparams
import numpy as np

#===========[ Methanogens Metabolism File for QHF  ]======================

# --- Initial version, Daniel Apai, Aug 1, 2023
#=========================================================================
def Methanogens_AEv1p0():
    global Module_Methanogens
    ModuleTemp = mcmodules.Module()
    ModuleTemp.define_name('Methanogens AE v1.0')
    ModuleTemp.add_input('Temperature')
    ModuleTemp.add_input('Pressure')
    ModuleTemp.add_output('Suitability')
    def _execute(self):
        #  Limits to enforce:
        #   suitability = 1 for 0.07 atm < P < 542.808 atm (55 MPa)
        #                       (273.25-16.0) < T < (273.25+122.0)
        #   suitability = 0 otherwise
        if (0.07 < keyparams.Pressure < 542.808) and ((273.25-16.0) < keyparams.Temperature < (273.25+122.)):
            keyparams.Suitability=1.0
        else:
            keyparams.Suitability=0.0
        print('Suitability calculated in module', keyparams.Suitability)
        # Key parameters are returned to the main function, allowing the Visualization
        # of the results. Below a dictionary is defined with the relevant values
        keyparams.runid = keyparams.runid+' | '+ ModuleTemp.name
        return

    ModuleTemp.execute = types.MethodType(_execute, ModuleTemp)
    ModuleTemp.activate()
    Module_Methanogens = ModuleTemp
    return Module_Methanogens
