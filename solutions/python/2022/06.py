def run(input_str):
    # Initial setup
    outputs = []

    # Part 1
    for i in range(len(input_str) - 4 + 1):
        if len(set(input_str[i : i + 4])) == len(input_str[i : i + 4]):
            outputs.append(i + 4)
            break

    # Part 2
    for i in range(len(input_str) - 14 + 1):
        if len(set(input_str[i : i + 14])) == len(input_str[i : i + 14]):
            outputs.append(i + 14)
            break

    return outputs
