def day_06(input_str):
    # Initial setup
    input_array = [i.split(" ") for i in input_str.replace("turn ", "").replace("through ", "").split("\n")]
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if j >= 1:
                input_array[i][j] = tuple(int(k) for k in input_array[i][j].split(","))
    outputs = []

    # Part 1
    lights = [[False]*1000 for i in range(1000)]
    for instruction in input_array:
        for i in range(instruction[1][0], instruction[2][0]+1):
            for j in range(instruction[1][1], instruction[2][1]+1):
                match instruction[0]:
                    case "on":
                        lights[i][j] = True
                    case "off":
                        lights[i][j] = False
                    case "toggle":
                        lights[i][j] = not lights[i][j]
    outputs.append(sum([sum(i) for i in lights]))

    # Part 2
    lights = [[0]*1000 for i in range(1000)]
    for instruction in input_array:
        for i in range(instruction[1][0], instruction[2][0]+1):
            for j in range(instruction[1][1], instruction[2][1]+1):
                match instruction[0]:
                    case "on":
                        lights[i][j] += 1
                    case "off":
                        lights[i][j] = max(0, lights[i][j]-1)
                    case "toggle":
                        lights[i][j] += 2
    outputs.append(sum([sum(i) for i in lights]))

    return outputs
