def run(input_str):
    # Initial setup
    input_array = input_str.split("\n")
    for i in range(len(input_array)):
        input_array[i] = int(input_array[i])
    outputs = []

    # Part 1
    outputs.append(0)
    for i in range(len(input_array) - 1):
        if input_array[i + 1] > input_array[i]:
            outputs[0] += 1

    # Part 2
    outputs.append(0)
    sums = []
    for i in range(len(input_array) - 2):
        sums.append(input_array[i] + input_array[i + 1] + input_array[i + 2])
    for i in range(len(sums) - 1):
        if sums[i + 1] > sums[i]:
            outputs[1] += 1

    return outputs
