def day_08(input_str):
    # Initial setup
    input_array = input_str.split("\n")
    outputs = []

    # Port 1
    total_diff = 0
    for code_str in input_array:
        total_diff += len(code_str) - eval(f"len({code_str})")
    outputs.append(total_diff)

    # Part 2
    new_diff = 0
    for code_str in input_array:
        new_diff += code_str.count("\"") + code_str.count("\\") + 2
    outputs.append(new_diff)

    return outputs
