def day_09(input_str):
    # Initial Setup
    input_array = [[int(j) for j in list(i)] for i in input_str.split("\n")]
    heightmap = input_array.copy()
    heightmap = [[10]*len(input_array[0])] + heightmap + [[10]*len(input_array[0])]
    for i in range(len(heightmap)):
        heightmap[i] = [10] + heightmap[i] + [10]
    outputs = []


    # Part 1
    total = 0
    for i in range(1, len(heightmap)-1):
        for j in range(1, len(heightmap[i])-1):
            isLow = True
            if heightmap[i][j] >= heightmap[i+1][j]:
                isLow = False
            elif heightmap[i][j] >= heightmap[i-1][j]:
                isLow = False
            elif heightmap[i][j] >= heightmap[i][j+1]:
                isLow = False
            elif heightmap[i][j] >= heightmap[i][j-1]:
                isLow = False
            if isLow == True:
                total += 1 + heightmap[i][j]
    outputs.append(total)


    # Part 2
    mappings = [[None for j in i] for i in heightmap]
    for i in range(1, len(heightmap)-1):
        for j in range(1, len(heightmap[i])-1):
            if heightmap[i][j] < 9:
                mappings[i][j] = (i, j)
    
    def replace_matching(old, new):
        for i in range(1, len(heightmap)-1):
            for j in range(1, len(heightmap[i])-1):
                if mappings[i][j] == old:
                    mappings[i][j] = new

    for height in range(8, -1, -1):
        for i in range(1, len(heightmap)-1):
            for j in range(1, len(heightmap[i])-1):
                if heightmap[i][j] == height:
                    if heightmap[i][j] > heightmap[i+1][j]:
                        replace_matching(mappings[i][j], (i+1, j))
                    elif heightmap[i][j] > heightmap[i-1][j]:
                        replace_matching(mappings[i][j], (i-1, j))
                    elif heightmap[i][j] > heightmap[i][j+1]:
                        replace_matching(mappings[i][j], (i, j+1))
                    elif heightmap[i][j] > heightmap[i][j-1]:
                        replace_matching(mappings[i][j], (i, j-1))
    
    counts = [[0 for j in i] for i in heightmap]
    for i in range(1, len(heightmap)-1):
        for j in range(1, len(heightmap[i])-1):
            if mappings[i][j] != None:
                counts[mappings[i][j][0]][mappings[i][j][1]] += 1
    
    sizes = []
    for i in range(1, len(heightmap)-1):
        for j in range(1, len(heightmap[i])-1):
            if counts[i][j] != 0:
                sizes.append(counts[i][j])
    sizes.sort(reverse=True)
    outputs.append(sizes[0] * sizes[1] * sizes[2])


    return outputs