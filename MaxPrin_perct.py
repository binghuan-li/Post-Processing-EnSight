'''
MaxPrin_perct.py

load this script in ANSYS EnSight to calcuate the 99 percentile of the max principal stress.
(or other scalar quantities)

BWL, 09/02/2026
'''

import numpy as np

#-----------------MODIFICATION START HERE-----------------
# 'wall':       <part name in EnSight>
# 'stress':     <variable name in EnSight>
setup = {
            'wall': 'Part 0', 
            'stress': 'Stress_maxprin_el'
        }
#-----------------MODIFICATION UNTIL HERE-----------------

ensight.variables.activate(setup['stress'])
ensight.solution_time.update_to_current()

part = ensight.objs.core.PARTS[setup['wall']][0]
coords = ensight.objs.core.VARIABLES['Coordinates'][0]
ws = part.get_values([coords,  setup['stress']], activate=1)
ws = ws[setup['stress']]

print(f'\t --->The 99 percentile of max principle stress is {np.percentile(ws, 99)}')
