def run(input_str):
    # Initial setup
    input_array = [[int(j) for j in i.split("x")] for i in input_str.split("\n")]
    outputs = []

    # Part 1
    total_area = 0
    for dimensions in input_array:
        side_areas = (
            dimensions[0] * dimensions[1],
            dimensions[1] * dimensions[2],
            dimensions[0] * dimensions[2],
        )
        total_area += 2 * sum(side_areas) + min(side_areas)
    outputs.append(total_area)

    # Part 2
    total_length = 0
    for dimensions in input_array:
        dimensions.sort()
        total_length += (
            2 * (dimensions[0] + dimensions[1])
            + dimensions[0] * dimensions[1] * dimensions[2]
        )
    outputs.append(total_length)

    return outputs
