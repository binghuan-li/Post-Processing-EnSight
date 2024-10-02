'''
load this script in ANSYS EnSight to filter the top 15% of velocity

calculate flow dispersion as per described in https://doi.org/10.1115/1.4037857

BWL, 27/09/2024
'''
import math

#---------------------------------------------
# only modify the following part
# <part ID>: <part name>
planes = {
    2: "AAINLET",
    9: "P1", 
    10: "P2", 
    11: "P3"
}
#---------------------------------------------

def get_centriod(part_name):
    p = ensight.query_parts([part_name])
    x_c = (p[0][2][0]+p[0][3][0])/2
    y_c = (p[0][2][1]+p[0][3][1])/2
    z_c = (p[0][2][2]+p[0][3][2])/2
    return [x_c, y_c, z_c]


percentile_to_keep = 0.85
flow_dispersion = []
flow_asymmetry = []

ensight.variables.activate("Velocity")

for i in planes.keys():
    # velocity magnitude
    ensight.part.select_begin(i)
    expr = "rms_velocity{} = RMS(Velocity)".format(i)
    ensight.variables.evaluate(expr)
    
    # max velocity
    ensight.part.select_begin(i)
    expr = "Max{} = Max(plist,rms_velocity{},[],Compute_Per_case)".format(i, i)
    ensight.variables.evaluate(expr)
    
    # min velocity
    ensight.part.select_begin(i)
    expr = "Min{} = Min(plist,rms_velocity{},[],Compute_Per_case)".format(i, i)
    ensight.variables.evaluate(expr)
    
    # threshold top 15% vel.
    ensight.part.select_begin(i)
    expr = "threshold_velocity{} = Min{}+{}*(Max{}-Min{})".format(i, i, percentile_to_keep, i, i)
    ensight.variables.evaluate(expr)
    
    # recover filtered velocity - not used but kept here for vel. visualisation purposes
    ensight.part.select_begin(i)
    expr = "vmax15_P{} = IF_GT(rms_velocity{}, threshold_velocity{})*Velocity".format(i, i, i)
    ensight.variables.evaluate(expr)
    
    # mask out the vel. below the threshold
    ensight.part.select_begin(i)
    expr = "nonzero_mask_P{} = IF_GT(rms_velocity{}, threshold_velocity{})".format(i, i, i)
    ensight.variables.evaluate(expr)
    
    # create Vmax15 isovoloume surfs
    ensight.isos.select_default()
    ensight.part.select_begin(i)
    ensight.isos.begin()
    ensight.part.description("Vmax15_P{}_mask".format(i))
    ensight.isos.variable("nonzero_mask_P{}".format(i))
    ensight.isos.end()
    ensight.isos.create()

    ensight.part.select_byname_begin("Vmax15_P{}_mask".format(i))
    ensight.part.modify_begin()
    ensight.isos.type("isovolume")
    ensight.isos.constraint("high")
    ensight.isos.max(1)
    ensight.part.modify_end()
    
    # get A_vmax15
    ensight.part.select_byname_begin("Vmax15_P{}_mask".format(i))
    ensight.variables.evaluate("Area_vmax15_P{} = Area(plist,Compute_Per_case)".format(i))
    
    # get A_plane
    ensight.part.select_begin(i)
    ensight.variables.evaluate("Area_P{} = Area(plist,Compute_Per_case)".format(i))
    
    Area_vmax15 = ensight.ensvariable("Area_vmax15_P{}".format(i))
    Area_P = ensight.ensvariable("Area_P{}".format(i))
    
    flow_dispersion.append((Area_vmax15[0]/Area_P[0])*100)
    
    # flow asymmetry
    x_a = get_centriod(planes[i])
    x_b = get_centriod("Vmax15_P{}_mask".format(i))
    d = math.dist(x_a, x_b)
    flow_asymmetry.append((d/math.sqrt(Area_P[0]/math.pi))*100)
    
print('done, report for flow dispersion and flow asymmetry.')
for i,j in enumerate (planes.keys()):
    print('plane {}, flow dispersion = {}%'.format(j, flow_dispersion[i]))
    print('plane {}, flow asymmetry = {}% \n'.format(j, flow_asymmetry[i]))