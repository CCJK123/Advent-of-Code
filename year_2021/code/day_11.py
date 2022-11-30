def day_11(input_str):
    # Initial Setup
    input_array = [[int(j) for j in list(i)]for i in input_str.split("\n")]
    
    def flashable(energy_lvls, has_flashed):
        is_flashable = False
        for i in range(1, len(energy_lvls)-1):
            for j in range(1, len(energy_lvls[i])-1):
                if energy_lvls[i][j] > 9 and has_flashed[i][j] == False:
                    is_flashable = True
        return is_flashable
    
    outputs = []


    # Part 1
    energy_lvls = input_array.copy()
    energy_lvls = [[-9]*len(input_array[0])] + energy_lvls + [[-9]*len(input_array[0])]
    for i in range(len(energy_lvls)):
        energy_lvls[i] = [-9] + energy_lvls[i] + [-9]
    
    flash_count = 0

    for step in range(100):
        has_flashed = [[False for j in i] for i in energy_lvls]
        energy_lvls = [[(j+1) for j in i] for i in energy_lvls]
        
        while flashable(energy_lvls, has_flashed):
            for i in range(1, len(energy_lvls)-1):
                for j in range(1, len(energy_lvls[i])-1):
                    if energy_lvls[i][j] > 9 and has_flashed[i][j] == False:
                        has_flashed[i][j] = True
                        for a in range(-1, 2):
                            for b in range(-1, 2):
                                energy_lvls[i+a][j+b] += 1
        
        for i in range(len(energy_lvls)):
            for j in range(len(energy_lvls[i])):
                if has_flashed[i][j] == True:
                    flash_count += 1
                    energy_lvls[i][j] = 0
                elif energy_lvls[i][j] < 0:
                    energy_lvls[i][j] = -9
    
    outputs.append(flash_count)


    # Part 2
    energy_lvls = input_array.copy()
    energy_lvls = [[-9]*len(input_array[0])] + energy_lvls + [[-9]*len(input_array[0])]
    for i in range(len(energy_lvls)):
        energy_lvls[i] = [-9] + energy_lvls[i] + [-9]
    
    synced_flashed = [[(False if j < 0 else True) for j in i] for i in energy_lvls]
    
    step = 0
    while True:
        has_flashed = [[False for j in i] for i in energy_lvls]
        energy_lvls = [[(j+1) for j in i] for i in energy_lvls]
        
        while flashable(energy_lvls, has_flashed):
            for i in range(1, len(energy_lvls)-1):
                for j in range(1, len(energy_lvls[i])-1):
                    if energy_lvls[i][j] > 9 and has_flashed[i][j] == False:
                        has_flashed[i][j] = True
                        for a in range(-1, 2):
                            for b in range(-1, 2):
                                energy_lvls[i+a][j+b] += 1
        
        step += 1
        if has_flashed == synced_flashed:
            break
        else:       
            for i in range(len(energy_lvls)):
                for j in range(len(energy_lvls[i])):
                    if has_flashed[i][j] == True:
                        energy_lvls[i][j] = 0
                    elif energy_lvls[i][j] < 0:
                        energy_lvls[i][j] = -9
    
    outputs.append(step)
    

    return outputs