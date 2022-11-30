def day_03(input_str):
    # Initial Setup
    input_array = input_str.split("\n")
    outputs = []


    # Part 1
    gamma_rate = ""
    epsilon_rate = ""
    remapped = []
    for i in range(len(input_array[0])):
        remapped.append([])
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            remapped[j].append(input_array[i][j])
    for i in remapped:
        if i.count("1") > i.count("0"):
            gamma_rate += "1"
            epsilon_rate += "0"
        else:
            gamma_rate += "0"
            epsilon_rate += "1"
    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)
    outputs.append(gamma_rate * epsilon_rate)


    # Part 2
    O2_rating = input_array.copy()
    CO2_rating = input_array.copy()
    O2_remapped = remapped.copy()
    CO2_remapped = remapped.copy()
    
    for i in range(len(remapped)):
        
        if O2_remapped[i].count("1") >= O2_remapped[i].count("0"):
            for j in O2_rating.copy():
                if len(O2_rating) > 1 and j[i] == "0":
                    O2_rating.remove(j)
        else:
            for j in O2_rating.copy():
                if len(O2_rating) > 1 and j[i] == "1":
                    O2_rating.remove(j)
        O2_remapped = []
        for j in range(len(remapped)):
            O2_remapped.append([])
        for j in range(len(O2_rating)):
            for k in range(len(O2_rating[j])):
                O2_remapped[k].append(O2_rating[j][k])

        if CO2_remapped[i].count("1") >= CO2_remapped[i].count("0"):
            for j in CO2_rating.copy():
                if len(CO2_rating) > 1 and j[i] == "1":
                    CO2_rating.remove(j)
        else:
            for j in CO2_rating.copy():
                if len(CO2_rating) > 1 and j[i] == "0":
                    CO2_rating.remove(j)
        CO2_remapped = []
        for j in range(len(remapped)):
            CO2_remapped.append([])
        for j in range(len(CO2_rating)):
            for k in range(len(CO2_rating[j])):
                CO2_remapped[k].append(CO2_rating[j][k])

    O2_rating = int(O2_rating[0], 2)
    CO2_rating = int(CO2_rating[0], 2)
    outputs.append(O2_rating * CO2_rating)
    
    
    return outputs