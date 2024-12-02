def run(input_str):
    # Initial setup
    input_array = input_str.split("\n")

    pipe_legend = {
        "|": ["north", "south"],
        "-": ["east", "west"],
        "L": ["north", "east"],
        "J": ["north", "west"],
        "7": ["south", "west"],
        "F": ["south", "east"],
    }
    direction_to_xy = {
        "north": (-1, 0),
        "south": (1, 0),
        "east": (0, 1),
        "west": (0, -1),
    }
    direction_inverse = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
    }

    outputs = []

    # Part 1
    ## Get start position
    start_coords = None
    for row_no, row in enumerate(input_array):
        if "S" in row:
            start_coords = (row_no, row.index("S"))
    assert start_coords is not None

    ## Get directions of pipes connected to start coords
    current_coords_list = []
    for direction, offset in direction_to_xy.items():
        test_coords = (start_coords[0] + offset[0], start_coords[1] + offset[1])
        if not all(i >= 0 for i in test_coords):
            continue
        possible_pipe = input_array[test_coords[0]][test_coords[1]]
        if possible_pipe not in pipe_legend.keys():
            continue
        if direction_inverse[direction] in pipe_legend[possible_pipe]:
            current_coords_list.append((start_coords, direction))
    assert len(current_coords_list) == 2

    ## Iterate through pipes to get max steps
    steps = 0
    while True:
        for current_coords, direction in current_coords_list.copy():
            offset = direction_to_xy[direction]
            future_coords = (
                current_coords[0] + offset[0],
                current_coords[1] + offset[1],
            )
            future_pipe = input_array[future_coords[0]][future_coords[1]]
            future_direction = pipe_legend[future_pipe].copy()
            future_direction.remove(direction_inverse[direction])
            future_direction = future_direction[0]
            current_coords_list.append((future_coords, future_direction))
            del current_coords_list[0]
        steps += 1
        if current_coords_list[0][0] == current_coords_list[1][0]:
            break
    outputs.append(steps)

    # Part 2
    ## Generate new map to differentiate inner from outer later
    pipe_map = [f".{row}." for row in input_array]
    pipe_map.insert(0, len(pipe_map[0]) * ".")
    pipe_map.append(len(pipe_map[0]) * ".")

    ## Get start position
    start_coords = None
    for row_no, row in enumerate(pipe_map):
        if "S" in row:
            start_coords = (row_no, row.index("S"))
    assert start_coords is not None
    coords_sets = {"pipe": {start_coords}, "left": set(), "right": set()}

    ## Get direction of a pipe connected to start coords
    start_direction = None
    for direction, offset in direction_to_xy.items():
        test_coords = (start_coords[0] + offset[0], start_coords[1] + offset[1])
        possible_pipe = pipe_map[test_coords[0]][test_coords[1]]
        if possible_pipe not in pipe_legend.keys():
            continue
        if direction_inverse[direction] in pipe_legend[possible_pipe]:
            start_direction = direction
            break
    assert start_direction is not None

    ## Iterate through pipe twice
    directions_clockwise = ["north", "east", "south", "west"]
    for stage in range(2):
        future_coords, future_direction = start_coords, start_direction
        while True:
            current_coords, current_direction = future_coords, future_direction
            if stage == 0:  # Get all pipe coords
                coords_sets["pipe"].add(current_coords)
            offset = direction_to_xy[current_direction]
            future_coords = (
                current_coords[0] + offset[0],
                current_coords[1] + offset[1],
            )
            if future_coords == start_coords:
                break
            future_pipe = pipe_map[future_coords[0]][future_coords[1]]
            future_direction = pipe_legend[future_pipe].copy()
            future_direction.remove(direction_inverse[current_direction])
            future_direction = future_direction[0]

            if stage == 1:  # Place left and right coords into respective coords sets
                for relative_direction, index_offset in (("left", -1), ("right", 1)):
                    offset = direction_to_xy[
                        directions_clockwise[
                            (
                                directions_clockwise.index(current_direction)
                                + index_offset
                            )
                            % 4
                        ]
                    ]
                    for coords in (current_coords, future_coords):
                        side_coords = (coords[0] + offset[0], coords[1] + offset[1])
                        if side_coords not in coords_sets["pipe"]:
                            coords_sets[relative_direction].add(side_coords)

    ## Propagate coords in left and right coords sets to include all coords in respective region
    for relative_direction in ("left", "right"):
        unchecked_coords_set = coords_sets[relative_direction].copy()
        while len(unchecked_coords_set) != 0:
            unchecked_coords = unchecked_coords_set.pop()
            for offset in direction_to_xy.values():
                test_coords = (
                    unchecked_coords[0] + offset[0],
                    unchecked_coords[1] + offset[1],
                )
                if (
                    (0 <= test_coords[0] <= (len(pipe_map) - 1))
                    and (0 <= test_coords[1] <= (len(pipe_map[0]) - 1))
                ) == False:
                    continue
                if test_coords not in coords_sets["pipe"].union(
                    coords_sets[relative_direction]
                ):
                    coords_sets[relative_direction].add(test_coords)
                    unchecked_coords_set.add(test_coords)
    assert sum(len(coord_set) for coord_set in coords_sets.values()) == (
        len(pipe_map) * len(pipe_map[0])
    )

    ## Determine which coords set corresponds to inner
    if (0, 0) in coords_sets["left"]:
        outputs.append(len(coords_sets["right"]))
    else:
        assert (0, 0) in coords_sets["right"]
        outputs.append(len(coords_sets["left"]))

    return outputs
