def day_09(input_str):
    # Initial setup
    import itertools
    input_array = [i.split(" = ") for i in input_str.split("\n")]
    for i in range(len(input_array)):
        input_array[i][0] = frozenset(input_array[i][0].split(" to "))
        input_array[i][1] = int(input_array[i][1])
    input_dict = dict(input_array)
    outputs = []

    # Parts 1 & 2 Combined
    locations = set()
    for path in input_array:
        locations = locations.union(path[0])
    distance_shortest, distance_longest = None, None
    for possible_route in itertools.permutations(locations, len(locations)):
        distance = 0
        for i in range(len(possible_route)-1):
            distance += input_dict[frozenset(possible_route[i:i+2])]
        # Part 1
        if distance_shortest is not None:
            if distance_shortest > distance:
                distance_shortest = distance
        else:
            distance_shortest = distance
        # Part 2
        if distance_longest is not None:
            if distance_longest < distance:
                distance_longest = distance
        else:
            distance_longest = distance
    outputs.extend([distance_shortest, distance_longest])

    return outputs
