'''
energy.py

Energy loss as per definition in Qiao et al. (2023)
https://doi.org/10.1016/j.ijengsci.2023.103939.

Note:
- currently this script only supports the EL calculation with one inlet and one outlet.

Binghuan Li, 19/05/2026
'''

parts = {# no need to change the name, keep 'in', 'out' as it is.
    "out": 7,
    "in": 14 
}
t = [0, 48]
Tcycle = 1

# var from ANSYS Fluent
velocity = "VELOCITY"
TP = "Total_Pressure"

for i in parts.keys():
    ensight.part.select_begin(parts[i])
    
    # Avg total pressure
    ensight.variables.evaluate(f"user_spamean_TP_{i} = SpaMean(plist,{TP},[],Compute_Per_case)")
    
    # flow rate
    ensight.variables.evaluate(f"user_Flow_{i}_m3s = Flow(plist,{velocity},Compute_Per_case)") 
    ensight.variables.evaluate(f"user_Flow_{i}_m3s_abs = ABS(user_Flow_{i}_m3s)")
    
# instantaneous power loss = TP * Q
ensight.variables.evaluate(
    f"user_PowerLoss_t_W = (user_spamean_TP_in * user_Flow_in_m3s_abs) - (user_spamean_TP_out * user_Flow_out_m3s_abs)"
)

# EL_total = Tcycle * TempMean of EL(t), convert into mJ
ensight.variables.evaluate(
    f"user_PowerLoss_mean_W = TempMean(plist,user_PowerLoss_t_W,{t[0]},{t[1]})"
)

ensight.variables.evaluate(
    f"user_EnergyLoss_cycle_J = user_PowerLoss_mean_W * {Tcycle}"
)

ensight.variables.evaluate(
    "user_EnergyLoss_cycle_mJ = user_EnergyLoss_cycle_J * 1000"
)

print("Done!")