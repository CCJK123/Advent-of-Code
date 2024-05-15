def day_17(input_str):
    # Initial setup
    import itertools
    input_array = [int(i) for i in input_str.split("\n")]
    outputs = []

    # Part 1
    combination_count = 0
    for container_count in range(len(input_array)):
        for combination in [i for i in itertools.combinations(input_array, container_count+1) if sum(i)==150]:
            combination_count += 1
    outputs.append(combination_count)
    
    # Part 2
    combination_count, min_containers = 0, len(input_array) + 1
    for container_count in range(len(input_array)):
        for combination in [i for i in itertools.combinations(input_array, container_count+1) if sum(i)==150]:
            min_containers = min(min_containers, len(combination))
    for combination in [i for i in itertools.combinations(input_array, min_containers) if sum(i)==150]:
            combination_count += 1
    outputs.append(combination_count)

    return outputs
