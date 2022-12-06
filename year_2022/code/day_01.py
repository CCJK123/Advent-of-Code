def day_01(input_str):
    # Initial setup
    input_array = [sum([int(j) for j in i.split("\n")])
                   for i in input_str.split("\n\n")]
    outputs = []

    # Part 1
    outputs.append(max(input_array))

    # Part 2
    temp_array = input_array.copy()
    temp_array.sort()
    outputs.append(sum(temp_array[-3:]))

    return outputs
