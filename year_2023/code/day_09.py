def day_09(input_str):
    # Initial setup
    input_array = [[int(j) for j in i.split(" ")] for i in input_str.split("\n")]
    outputs = []

    # Part 1 & 2 Combined
    value_sum = value_sum_2 = 0

    for value_history in input_array:
        differences_list = []
        differences = value_history

        while set(differences) != {0}:
            differences_list.insert(0, differences)
            new_differences = []
            for i in range(len(differences) - 1):
                new_differences.append(differences[i + 1] - differences[i])
            differences = new_differences

        # Part 1
        for i in range(len(differences_list) - 1):
            differences_list[i + 1].append(
                differences_list[i + 1][-1] + differences_list[i][-1]
            )
        value_sum += differences_list[-1][-1]

        # Part 2
        for i in range(len(differences_list) - 1):
            differences_list[i + 1].insert(
                0, differences_list[i + 1][0] - differences_list[i][0]
            )
        value_sum_2 += differences_list[-1][0]

    outputs.append(value_sum)
    outputs.append(value_sum_2)

    return outputs
