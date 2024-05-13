def day_03(input_str):
    # Initial setup
    outputs = []

    # Part 1
    coords, presents = [0, 0], {(0, 0): 1}
    for direction in input_str:
        match direction:
            case "^":
                coords[1] += 1
            case "v":
                coords[1] -= 1
            case ">":
                coords[0] += 1
            case "<":
                coords[0] -= 1
        if tuple(coords) in presents.keys():
            presents[tuple(coords)] += 1
        else:
            presents[tuple(coords)] = 1
    outputs.append(len(presents))

    # Part 2
    presents = {(0, 0): 2}
    for directions in (input_str[::2], input_str[1::2]):
        coords = [0, 0]
        for direction in directions:
            match direction:
                case "^":
                    coords[1] += 1
                case "v":
                    coords[1] -= 1
                case ">":
                    coords[0] += 1
                case "<":
                    coords[0] -= 1
            if tuple(coords) in presents.keys():
                presents[tuple(coords)] += 1
            else:
                presents[tuple(coords)] = 1
    outputs.append(len(presents))

    return outputs
