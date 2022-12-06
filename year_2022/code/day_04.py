def day_04(input_str):
    # Initial setup
    input_array = [[j.split("-") for j in i.split(",")]
                   for i in input_str.split("\n")]
    for i in range(len(input_array)):
        for j in range(2):
            input_array[i][j] = set(
                range(int(input_array[i][j][0]), int(input_array[i][j][1])+1)
            )
    outputs = []

    # Part 1
    count = 0
    for pair in input_array:
        if pair[0].issubset(pair[1]) or pair[1].issubset(pair[0]):
            count += 1
    outputs.append(count)

    # Part 2
    count = 0
    for pair in input_array:
        if pair[0].intersection(pair[1]) != set():
            count += 1
    outputs.append(count)

    return outputs
