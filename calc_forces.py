'''
load this script in ANSYS EnSight to calcuate the displacement force

partial code taken from net_force.py provided by the EnSight distribution.

Notes:
    - modify the global variables declared at the top of this script only.
    - calculation is slow by looping through all time steps, use with discretion.
    
BWL, 07/10/2024
'''
import numpy as np
import os

# case specific global variables to modify
#-----------------START HERE-----------------
PART_ID = 6
T_START = 1
T_END = 2

SAVE_PATH = 'C:/Users/lbing/Desktop/'

WSS_NAME = "Wall_Shear"
PRES_NAME = "Pressure"
#-----------------UNTIL HERE-----------------

def calc_var(PART_ID, calc_string):
#
# calculate variables in EnSight, non-zero return indicates error
#
    ensight.part.select_begin(PART_ID)
    err = ensight.variables.evaluate(calc_string)
    return err
    
def calc_shear():
#
# decompose the wall shear into the normal and tangential directions,
# and calculate shear force from shear stress.
#

    # Compute normal and tangential components of wall shear
    temp_string = "ENS_Force_Dot_prod_Flu_shear_Stress_Norm = DOT({},ENS_Force_Norm)".format(WSS_NAME)
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_Dot_prod_Flu_shear_Stress_Norm")

    temp_string = "ENS_Force_NomalShearStress = ENS_Force_Dot_prod_Flu_shear_Stress_Norm*ENS_Force_Norm"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_NomalShearStress")

    temp_string = "ENS_Force_TangentialShearStress = {} - ENS_Force_NomalShearStress".format(WSS_NAME)
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_TangentialShearStress")


    # Decompose the TangentialShearStress Vector into its x, y, z components
    temp_string = "ENS_Force_TangentialShearStress_X = ENS_Force_TangentialShearStress[X]"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_TangentialShearStress_X")

    temp_string = "ENS_Force_TangentialShearStress_Y = ENS_Force_TangentialShearStress[Y]"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_TangentialShearStress_Y")

    temp_string = "ENS_Force_TangentialShearStress_Z = ENS_Force_TangentialShearStress[Z]"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_TangentialShearStress_Z")

    # Calculate the Tangential Shear stress forces
    temp_string = "ENS_Force_ElementArea = EleSize(plist)"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_ElementArea")

    temp_string = "ENS_Force_Tan_ShearForce_X = ENS_Force_TangentialShearStress_X*ENS_Force_ElementArea"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_Tan_ShearForce_X")

    temp_string = "ENS_Force_Tan_ShearForce_Y = ENS_Force_TangentialShearStress_Y*ENS_Force_ElementArea"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_Tan_ShearForce_Y")

    temp_string = "ENS_Force_Tan_ShearForce_Z = ENS_Force_TangentialShearStress_Z*ENS_Force_ElementArea"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_Tan_ShearForce_Z")
        
    # Calculate the Total force X, Y, and Z
    temp_string = "ENS_Force_Total_Net_Tan_ShearForce_X = StatMoment(plist,ENS_Force_Tan_ShearForce_X, 0, Compute_Per_case)"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_Total_Net_Tan_ShearForce_X")
    
    temp_string = "ENS_Force_Total_Net_Tan_ShearForce_Y = StatMoment(plist,ENS_Force_Tan_ShearForce_Y, 0, Compute_Per_case)"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_Total_Net_Tan_ShearForce_Y")

    temp_string = "ENS_Force_Total_Net_Tan_ShearForce_Z = StatMoment(plist,ENS_Force_Tan_ShearForce_Z, 0, Compute_Per_case)"
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_Total_Net_Tan_ShearForce_Z")    
    
    # calculate total WSS force
    Ftx = ensight.ensvariable("ENS_Force_Total_Net_Tan_ShearForce_X")
    Fty = ensight.ensvariable("ENS_Force_Total_Net_Tan_ShearForce_Y")
    Ftz = ensight.ensvariable("ENS_Force_Total_Net_Tan_ShearForce_Z")
    
    Ft = [Ftx[0], Fty[0], Ftz[0]]
    
    return np.array(Ft)
        
        
def calc_pres():
#
# calculate pressure force from pressure
#
    calc_string = "ENS_Force_press = Force(plist, {})".format(PRES_NAME)
    if 0 != calc_var(PART_ID,calc_string):
        print("error in ENS_Force_press")

    # Calculate the force components
    temp_string = 'ENS_Force_press_X = ENS_Force_press[X]'
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_press_X")

    temp_string = 'ENS_Force_press_Y = ENS_Force_press[Y]'
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_press_Y")

    temp_string = 'ENS_Force_press_Z = ENS_Force_press[Z]'
    if 0 != calc_var(PART_ID,temp_string):
        print("error in ENS_Force_press_Z")
    
    # Calculate the net force X, Y, and Z
    calc_string = "ENS_Force_Net_press_X = StatMoment(plist, ENS_Force_press_X , 0, Compute_Per_part)"
    if 0 != calc_var(PART_ID,calc_string):
         print("error in ENS_Force_Net_press_X")
        
    calc_string = "ENS_Force_Net_press_Y = StatMoment(plist, ENS_Force_press_Y , 0, Compute_Per_part)"
    if 0 != calc_var(PART_ID,calc_string):
         print("error in ENS_Force_Net_press_Y")
    
    calc_string = "ENS_Force_Net_press_Z = StatMoment(plist, ENS_Force_press_Z , 0, Compute_Per_part)"
    if 0 != calc_var(PART_ID,calc_string):
         print("error in ENS_Force_Net_press_Z")
        
    # Calculate the Total force X, Y, and Z
    calc_string = "ENS_Force_Total_Net_press_X = StatMoment(plist, ENS_Force_press_X , 0, Compute_Per_case )"
    if 0 != calc_var(PART_ID,calc_string):
         print("error in ENS_Force_Total_Net_press_X")
    
    calc_string = "ENS_Force_Total_Net_press_Y = StatMoment(plist, ENS_Force_press_Y , 0, Compute_Per_case )"
    if 0 != calc_var(PART_ID,calc_string):
         print("error in ENS_Force_Total_Net_press_Y")
    
    calc_string = "ENS_Force_Total_Net_press_Z = StatMoment(plist, ENS_Force_press_Z , 0, Compute_Per_case )"
    if 0 != calc_var(PART_ID,calc_string):
         print("error in ENS_Force_Total_Net_press_Z")
    
    # calculate total pressure force
    Fpx = ensight.ensvariable("ENS_Force_Total_Net_press_X")
    Fpy = ensight.ensvariable("ENS_Force_Total_Net_press_Y")
    Fpz = ensight.ensvariable("ENS_Force_Total_Net_press_Z")
    
    Fp = [Fpx[0], Fpy[0], Fpz[0]]
    
    return np.array(Fp)

def move_to_element():
#
# wall shear and pressure are nodal vars, need to map onto each element  
# Wall_Shear --> Wall_Shear_E
# Pressure --> Pressure_E
#
    ensight.part.select_begin(PART_ID)
    for var in [WSS_NAME, PRES_NAME]:
        expr = "{}_E = NodeToElem(plist,{})".format(var, var) 
        if 0 != calc_var(PART_ID, expr):
            print("error in move_to_element")
         

def calc_vec_magn(vec):
#
# calculate magnitude of a 3-element vevtor [v_x, v_y, v_z]
#
    mag = np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
    return mag;


def run_for_transition():
#
# Use this with discretion - can be slow.
#

    force = [];
        
    for i in range(T_START, T_END):

        # sync to the current step
        ensight.solution_time.current_step(float(i))
        ensight.solution_time.update_to_current()
        
        # do calc
        ensight.part.select_begin(PART_ID)
        move_to_element();
        Ft = calc_shear();
        Fp = calc_pres();
        F_tot = Fp + Ft;
        F_tot_mag = calc_vec_magn(F_tot)
        force.append(F_tot_mag);
        
    with open(os.path.join(SAVE_PATH, "Ftotal.txt"), 'w') as f:
        for i in force:
            print(i)
            f.write(str(i)+'\n')


# create a surface normal vector variable
temp_string = "ENS_Force_Norm = Normal(plist)"
if 0 != calc_var(PART_ID,temp_string):
    print("error in ENS_Force_Norm")
run_for_transition();