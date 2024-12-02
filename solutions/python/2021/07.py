def run(input_str):
    # Initial Setup
    input_array = input_str.split(",")
    input_array = [int(i) for i in input_array]
    outputs = []

    # Part 1
    costs = [0] * (max(input_array) + 1)
    for i in range(len(costs)):
        for j in input_array:
            costs[i] += abs(i - j)
    outputs.append(min(costs))

    # Part 2
    def one_to_x_sum(x):
        return int((x + 1) * (x / 2))

    costs = [0] * (max(input_array) + 1)
    for i in range(len(costs)):
        for j in input_array:
            costs[i] += one_to_x_sum(abs(i - j))
    outputs.append(min(costs))

    return outputs
