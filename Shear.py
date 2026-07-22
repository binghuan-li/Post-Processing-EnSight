'''
Shear.py

load this script in ANSYS EnSight to calcuate the haemodynamic variables.

Notes:
    - flow of execulation should follow the same order as the scripts presents
    - only modify the global variables declared at the top of the scirpt
    - if the output wall shear vectors are stored at the element, move to node first
    
BWL, 02/10/2024, 05/03/2025
'''
#---------------------------------------
# MODIFY THE FOLLOWING GLOBAL VARIABLES
#---------------------------------------
start_pt = 1;
end_pt = 48;
wall_part_ID = 2;
var_names = {
    "wss": "WALL_SHEAR_STRESS"
};
to_node = True;
#---------------------------------------
#---------------------------------------
print("Calculations begin");

# rewind current time step the beginning
ensight.solution_time.current_step(0.);
ensight.solution_time.update_to_current();

ensight.variables.activate(f"{var_names['wss']}");

# element to node
if to_node:
    ensight.variables.activate(f"{var_names['wss']}");
    ensight.variables.evaluate(f"user_WALL_SHEAR_STRESS = ElemToNode(plist,{var_names['wss']})");
    var_names['wss'] = "user_WALL_SHEAR_STRESS";

#
# TAWSS
#
ensight.variables.evaluate(f"user_INTERM_rms_wall_shear = RMS({var_names['wss']})");
ensight.part.select_begin(wall_part_ID);
err = ensight.variables.evaluate(f"user_TAWSS = TempMean(plist,user_INTERM_rms_wall_shear,{start_pt},{end_pt})");
if err == 0:
    print("\t--> TAWSS calculation successful!");
else:
    raise Exception("AN UNKNOWN ERROR RAISED WHEN TRYING TO CALCULATE TAWSS.");

#
# OSI
#
ensight.variables.evaluate(f"user_INTERM_TempMean_wss = TempMean(plist,{var_names['wss']},{start_pt},{end_pt})");
ensight.part.select_begin(wall_part_ID);
ensight.variables.evaluate("user_INTERM_rms_tempmean_wss = RMS(user_INTERM_TempMean_wss)");
ensight.part.select_begin(wall_part_ID);
err = ensight.variables.evaluate("user_OSI = 0.5 * ( 1 - (user_INTERM_rms_tempmean_wss/user_TAWSS))");
if err == 0:
    print("\t--> OSI calculation successful!");
else:
    raise Exception("AN UNKNOWN ERROR RAISED WHEN TRYING TO CALCULATE OSI.");

#
# ECAP
#
ensight.part.select_begin(wall_part_ID);
err = ensight.variables.evaluate("user_ECAP = user_OSI/user_TAWSS");
if err == 0:
    print("\t--> ECAP calculation successful!");
else:
    raise Exception("AN UNKNOWN ERROR RAISED WHEN TRYING TO CALCULATE ECAP.");

#
# RRT
#
ensight.part.select_begin(wall_part_ID);
err = ensight.variables.evaluate("user_RRT = 1/((1 - 2*user_OSI) *user_TAWSS)");
if err == 0:
    print("\t--> RRT calculation successful!");
else:
    raise Exception("AN UNKNOWN ERROR RAISED WHEN TRYING TO CALCULATE RRT.");

#
# TransWSS
#
ensight.part.select_begin(wall_part_ID);
ensight.variables.evaluate("user_INTERM_transwss_inner_frac = user_INTERM_TempMean_wss/user_INTERM_rms_wall_shear");
ensight.part.select_begin(wall_part_ID);
ensight.variables.evaluate("user_INTERM_transwss_norm_of_frac = NormVect(plist,user_INTERM_transwss_inner_frac)");
ensight.part.select_begin(wall_part_ID);
ensight.variables.evaluate(f"user_INTERM_transwss_rms_of_norm = ABS(DOT({var_names['wss']}, user_INTERM_transwss_norm_of_frac))");
ensight.part.select_begin(wall_part_ID);
err = ensight.variables.evaluate(f"user_TransWSS = TempMean(plist,user_INTERM_transwss_rms_of_norm,{start_pt},{end_pt})");
if err == 0:
    print("\t--> TransWSS calculation successful!");
else:
    raise Exception("AN UNKNOWN ERROR RAISED WHEN TRYING TO CALCULATE TransWSS.");

#
# CFI
#
ensight.part.select_begin(wall_part_ID);
ensight.variables.evaluate(f"user_INTERM_CFI_integrand = ({var_names['wss']}/RMS({var_names['wss']}))* user_INTERM_transwss_norm_of_frac");
ensight.part.select_begin(wall_part_ID);
err = ensight.variables.evaluate(f"user_CFI = TempMean(plist,user_INTERM_CFI_integrand,{start_pt},{end_pt})");
if err == 0:
    print("\t--> CFI calculation successful!");
else:
    raise Exception("AN UNKNOWN ERROR RAISED WHEN TRYING TO CALCULATE CFI.");

print("Done");
