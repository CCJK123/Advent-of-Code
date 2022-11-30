def day_05(input_str):
    # Initial Setup
    input_array = input_str.split("\n")
    input_array = [i.split(" -> ") for i in input_array]
    for i in range(len(input_array)):
        #input_array[i] = [j.split(",") for j in input_array[i]]
        for j in range(len(input_array[i])):
            input_array[i][j] = input_array[i][j].split(",")
            for k in range(len(input_array[i][j])):
                input_array[i][j][k] = int(input_array[i][j][k])
    outputs = []
    

    # Part 1
    max_xy = [0, 0]
    for i in input_array:
        for j in i:
            for k in range(2):
                max_xy[k] = max(j[k], max_xy[k])
    vents = [[0 for j in range(max_xy[1]+1)] for i in range(max_xy[0]+1)]
    
    for i in input_array:
        if i[0][0] == i[1][0]:
            # x-coords match
            for j in range(min(i[0][1], i[1][1]), max(i[0][1], i[1][1]) + 1):
                vents[i[0][0]][j] += 1
        elif i[0][1] == i[1][1]:
            # y-coords match
            for j in range(min(i[0][0], i[1][0]), max(i[0][0], i[1][0]) + 1):
                vents[j][i[0][1]] += 1
    
    overlaps = 0
    for i in vents:
        for j in i:
            if j >= 2:
                overlaps += 1
    outputs.append(overlaps)


    # Part 2
    for i in input_array:

        if i[0][0] == i[1][0]:
            # x-coords match (handled above)
            pass

        elif i[0][1] == i[1][1]:
            # y-coords match (handled above)
            pass

        elif (i[0][0] - i[1][0]) == (i[0][1] - i[1][1]):
            # xy-both-increase/decrease diagonal
            for j in range(0, max(i[0][0], i[1][0])-min(i[0][0], i[1][0])+1):
                vents[max(i[0][0], i[1][0])-j][max(i[0][1], i[1][1])-j] += 1
        
        elif (i[0][0] - i[1][0]) == -(i[0][1] - i[1][1]):
            # flip-flop diagonal
            if i[0][0] <= i[1][0]:
                # x-increase, y-decrease
                for j in range(0, max(i[0][0], i[1][0])-min(i[0][0], i[1][0])+1):
                    vents[min(i[0][0], i[1][0])+j][max(i[0][1], i[1][1])-j] += 1
            else:
                # x-decrease, y-increase
                for j in range(0, max(i[0][0], i[1][0])-min(i[0][0], i[1][0])+1):
                    vents[max(i[0][0], i[1][0])-j][min(i[0][1], i[1][1])+j] += 1

    overlaps = 0
    for i in vents:
        for j in i:
            if j >= 2:
                overlaps += 1
    outputs.append(overlaps)


    return outputs