def run(input_str):
    # Initial setup
    input_array = input_str.split("\n")
    for i in range(len(input_array)):
        input_array[i] = input_array[i].split(" ")
        input_array[i][1] = int(input_array[i][1])
    outputs = []

    # Part 1
    horizontal_dist = 0
    depth = 0
    for command in input_array:
        if command[0] == "forward":
            horizontal_dist += command[1]
        elif command[0] == "down":
            depth += command[1]
        elif command[0] == "up":
            depth -= command[1]
    outputs.append(horizontal_dist * depth)

    # Part 2
    horizontal_dist = 0
    depth = 0
    aim = 0
    for command in input_array:
        if command[0] == "forward":
            horizontal_dist += command[1]
            depth += aim * command[1]
        elif command[0] == "down":
            aim += command[1]
        elif command[0] == "up":
            aim -= command[1]
    outputs.append(horizontal_dist * depth)

    return outputs
