def day_10(input_str):
    # Initial setup
    import copy
    input_array = [i.split() for i in input_str.split("\n")]
    for i in range(len(input_array)):
        if input_array[i][0] == "addx":
            input_array[i][1] = int(input_array[i][1])
    outputs = []

    # Part 1
    instructions = copy.deepcopy(input_array)
    for i in range(len(instructions)):
        if instructions[i][0] == "addx":
            instructions[i].append(2)

    cycle_num = 0
    register_X = 1
    signal_strength_sum = 0
    while instructions != []:
        cycle_num += 1
        # During cycle (calculate signal strength when required)
        if cycle_num in range(20, 221, 40):
            signal_strength_sum += cycle_num * register_X
        # After cycle (handling of instructions and register X)
        if instructions[0][0] == "noop":
            instructions.pop(0)
        elif instructions[0][0] == "addx":
            instructions[0][2] -= 1
            if instructions[0][2] == 0:
                register_X += instructions[0][1]
                instructions.pop(0)

    outputs.append(signal_strength_sum)

    # Part 2
    instructions = copy.deepcopy(input_array)
    for i in range(len(instructions)):
        if instructions[i][0] == "addx":
            instructions[i].append(2)

    cycle_num = 0
    register_X = 1
    CRT_image = "(the 8 capital letters below)\n"
    while instructions != []:
        cycle_num += 1
        # During cycle (draw pixel on CRT)
        if ((cycle_num-1) % 40) in range(register_X-1, register_X+2):
            CRT_image += "#"
        else:
            CRT_image += " "
        if cycle_num % 40 == 0:
            CRT_image += "\n"
        # After cycle (handling of instructions and register X)
        if instructions[0][0] == "noop":
            instructions.pop(0)
        elif instructions[0][0] == "addx":
            instructions[0][2] -= 1
            if instructions[0][2] == 0:
                register_X += instructions[0][1]
                instructions.pop(0)

    outputs.append(CRT_image)

    return outputs
