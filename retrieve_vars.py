'''
load this script in ANSYS EnSight to calcuate the haemodynamic variables.

Notes:
    - flow of execulation should follow the same order as the scripts presents
    - modify only the global variables at the top of the scirpt
    
BWL, 02/10/2024
'''

# case specific global variables to modify
#-----------------START HERE-----------------
start_pt = 1;
end_pt = 99;
wall_part_ID = 6;
vol_part_ID = 1;
#-----------------UNTIL HERE-----------------

print('Calculation begins')

# calculate TAWSS
ensight.variables.activate("Wall_Shear")
ensight.variables.evaluate("rms_wall_shear = RMS(Wall_Shear)")
ensight.part.select_begin(wall_part_ID)
expr = "TAWSS = TempMean(plist,rms_wall_shear,{},{})".format(start_pt, end_pt)
err = ensight.variables.evaluate(expr)
if err == 0:
    print('--> TAWSS calculation successful!')

# calculate OSI
expr = "TempMean_wss = TempMean(plist,Wall_Shear,{},{})".format(start_pt, end_pt)
ensight.variables.evaluate(expr)
ensight.part.select_begin(wall_part_ID)
ensight.variables.evaluate("rms_tempmean_wss = RMS(TempMean_wss)")
ensight.part.select_begin(wall_part_ID)
err = ensight.variables.evaluate("OSI = 0.5 * ( 1 - (rms_tempmean_wss/TAWSS))")
if err == 0:
    print('--> OSI calculation successful!')

# calculate ECAP
ensight.part.select_begin(wall_part_ID)
err = ensight.variables.evaluate("ECAP = OSI/TAWSS")
if err == 0:
    print('--> ECAP calculation successful!')

# calculate RRT
ensight.part.select_begin(wall_part_ID)
err = ensight.variables.evaluate("RRT = 1/((1 - 2*OSI) *TAWSS)")
if err == 0:
    print('--> RRT calculation successful!')

# calculate TransWSS
ensight.part.select_begin(wall_part_ID)
ensight.variables.evaluate("transwss_inner_frac = TempMean_wss/rms_wall_shear")
ensight.part.select_begin(wall_part_ID)
ensight.variables.evaluate("transwss_norm_of_frac = NormVect(plist,transwss_inner_frac)")
ensight.part.select_begin(wall_part_ID)
ensight.variables.evaluate("transwss_rms_of_norm = ABS(DOT(Wall_Shear, transwss_norm_of_frac))")
ensight.part.select_begin(wall_part_ID)
expr = "TransWSS = TempMean(plist,transwss_rms_of_norm,{},{})".format(start_pt, end_pt)
err = ensight.variables.evaluate(expr)
if err == 0:
    print('--> TransWSS calculation successful!')

# calculate cross flow index
ensight.part.select_begin(wall_part_ID)
ensight.variables.evaluate("CFI_integrand = (Wall_Shear/RMS(Wall_Shear))* transwss_norm_of_frac")
ensight.part.select_begin(wall_part_ID)
expr = "CFI = TempMean(plist,CFI_integrand,{},{})".format(start_pt, end_pt)
err = ensight.variables.evaluate(expr)
if err == 0:
    print('--> CFI calculation successful!')

# calculate turbulence intensity
ensight.part.select_begin(vol_part_ID)
ensight.variables.activate("Turbulence_Kinetic_Energy")
err = ensight.variables.evaluate("TI = SQRT((2/3) * Turbulence_Kinetic_Energy)/Velocity")
if err == 0:
    print('--> TI calculation successful!')

print('Done')