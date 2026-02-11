'''
WSS_perct.py

load this script in ANSYS EnSight to calcuate the 99 percentile of the wall shear stress.
(or other vector quantities)

BWL, 09/02/2026
'''

import numpy as np

#-----------------MODIFICATION START HERE-----------------
# 'wall':       <part name in EnSight>
# 'wall_shear': <variable name in EnSight>
setup = {
            'wall': 'wall', 
            'wall_shear': 'Wall_Shear'
        }
#-----------------MODIFICATION UNTIL HERE-----------------

ensight.variables.activate(setup['wall_shear'])
ensight.solution_time.update_to_current()

part = ensight.objs.core.PARTS[setup['wall']][0]
coords = ensight.objs.core.VARIABLES['Coordinates'][0]
wss = part.get_values([coords,  setup['wall_shear']], activate=1) # returned as a dict
wss = np.linalg.norm(wss[setup['wall_shear']], axis=1) # unpack and calc the mag

print(f'\t --->The 99 percentile of wss is {np.percentile(wss, 99)}')
