## calculate mean flow rate

parts = {
    "inlet": 4,
    "daout": 3,
    "iaout": 7,
    "lccaout": 5,
    "lscaout": 6
}

t = [0, 198]
velocity = "VELOCITY"

for i in parts.keys():
    print(i, parts[i])
    ensight.part.select_begin(parts[i])
    ensight.variables.evaluate(f"FlowRate_{i} = FlowRate(plist,{velocity})")
    ensight.variables.evaluate(f"sum_flow_rate_{i} = sumPerPart(plist,FlowRate_{i},Compute_Per_case)")
    ensight.variables.evaluate(f"mean_flow_{i} = TempMean(plist,sum_flow_rate_{i},{t[0]},{t[1]})")