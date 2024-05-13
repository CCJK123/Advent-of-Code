def day_01(input_str):
    # Initial setup
    outputs = []

    # Part 1
    outputs.append(input_str.count("(") - input_str.count(")"))

    # Part 2
    floor = 0
    for position in range(len(input_str)):
        if input_str[position] == "(":
            floor += 1
        else:
            floor -= 1
        
        if floor == -1:
            outputs.append(position + 1)
            break

    return outputs
