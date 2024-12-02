def run(input_str):
    # Initial setup
    import numpy as np

    input_array = [
        [[int(k) for k in j.split(",")] for j in i.split(" -> ")]
        for i in input_str.split("\n")
    ]
    outputs = []

    def show_cave_map(cave_map):
        symbol_reference = {
            "air": ".",
            "rock": "#",
            "sand_fallen": "o",
            "sand_source": "+",
        }
        for y, row in enumerate(np.transpose(cave_map)):
            to_print = ""
            for x, column in enumerate(row):
                if x >= len(cave_map) - 25:
                    to_print += symbol_reference[column]
            print(to_print, y)

    # Part 1
    # # Generate map of cave
    max_coords = np.array([500, 0])
    for rock_path in input_array:
        for rock_corner in rock_path:
            max_coords = np.maximum(max_coords, rock_corner)
    cave_map = np.array(
        [["air"] * (max_coords[1] + 1 + 1)] * (max_coords[0] + 1 + 1), dtype=object
    )

    # # Add cave features (sand source and rock) to map
    cave_map[500, 0] = "sand_source"
    for rock_path in input_array:
        for rock_corner_num in range(len(rock_path) - 1):
            cave_map[
                min(
                    rock_path[rock_corner_num][0], rock_path[rock_corner_num + 1][0]
                ) : max(
                    rock_path[rock_corner_num][0], rock_path[rock_corner_num + 1][0]
                )
                + 1,
                min(
                    rock_path[rock_corner_num][1], rock_path[rock_corner_num + 1][1]
                ) : max(
                    rock_path[rock_corner_num][1], rock_path[rock_corner_num + 1][1]
                )
                + 1,
            ] = "rock"

    # # Simulate sand
    total_units_of_sand = 0
    falling_sand_coords = np.array([500, 0])

    while True:
        if falling_sand_coords[1] > max_coords[1]:
            # Current falling sand unit is not within boundaries
            # (i.e. stop spawning new sand units)
            break

        else:
            # Calculate current sand unit's movement
            if cave_map[tuple(falling_sand_coords + (0, 1))] == "air":
                # Can fall vertically down, move there
                falling_sand_coords += (0, 1)
            elif cave_map[tuple(falling_sand_coords + (-1, 1))] == "air":
                # Can fall down and to the left
                falling_sand_coords += (-1, 1)
            elif cave_map[tuple(falling_sand_coords + (1, 1))] == "air":
                # Can fall down and to the right
                falling_sand_coords += (1, 1)
            else:
                # Cannot fall down at all (i.e. it's in a fixed location)
                # # Place down sand on map
                cave_map[tuple(falling_sand_coords)] = "sand_fallen"
                total_units_of_sand += 1
                # # Spawn new unit of sand
                falling_sand_coords = np.array([500, 0])

    # show_cave_map(cave_map)
    outputs.append(total_units_of_sand)

    # Part 2
    # # Generate map of cave
    # # # Calculate max coords
    max_coords = np.array([500, 0])
    for rock_path in input_array:
        for rock_corner in rock_path:
            max_coords = np.maximum(max_coords, rock_corner)
    # # # Account for floor (which also causes increased sand spread)
    max_coords += (0, 2)
    max_coords[0] = max(500 + max_coords[1], max_coords[0])
    # # # Create map of cave
    cave_map = np.array(
        [["air"] * (max_coords[1] + 1)] * (max_coords[0] + 1), dtype=object
    )

    # # Add cave features (sand source and rock (paths and floor)) to map
    cave_map[500, 0] = "sand_source"
    for rock_path in input_array:
        for rock_corner_num in range(len(rock_path) - 1):
            cave_map[
                min(
                    rock_path[rock_corner_num][0], rock_path[rock_corner_num + 1][0]
                ) : max(
                    rock_path[rock_corner_num][0], rock_path[rock_corner_num + 1][0]
                )
                + 1,
                min(
                    rock_path[rock_corner_num][1], rock_path[rock_corner_num + 1][1]
                ) : max(
                    rock_path[rock_corner_num][1], rock_path[rock_corner_num + 1][1]
                )
                + 1,
            ] = "rock"
    cave_map[: len(cave_map) + 1, max_coords[1]] = "rock"

    # # Simulate sand
    total_units_of_sand = 0
    falling_sand_coords = np.array([500, 0])

    while True:
        # Check if current sand unit can fall
        if cave_map[tuple(falling_sand_coords + (0, 1))] == "air":
            # Can fall vertically down, move there
            falling_sand_coords += (0, 1)
        elif cave_map[tuple(falling_sand_coords + (-1, 1))] == "air":
            # Can fall down and to the left
            falling_sand_coords += (-1, 1)
        elif cave_map[tuple(falling_sand_coords + (1, 1))] == "air":
            # Can fall down and to the right
            falling_sand_coords += (1, 1)

        # Check if sand source is blocked
        elif cave_map[tuple(falling_sand_coords)] == "sand_source":
            # Current falling sand unit cannot fall and is at coords of sand source
            # (i.e. sand source is blocked, stop spawning new sand units)
            cave_map[tuple(falling_sand_coords)] = "sand_fallen"
            total_units_of_sand += 1
            break

        # Cannot fall down at all (i.e. it's in a fixed location)
        else:
            # Place down sand on map
            cave_map[tuple(falling_sand_coords)] = "sand_fallen"
            total_units_of_sand += 1
            # Spawn new unit of sand
            falling_sand_coords = np.array([500, 0])

    # show_cave_map(cave_map)
    outputs.append(total_units_of_sand)

    return outputs
