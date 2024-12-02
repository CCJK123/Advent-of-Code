def run(input_str):
    # Initial setup
    import numpy as np

    input_array = [i.split() for i in input_str.split("\n")]
    for i in range(len(input_array)):
        input_array[i][1] = int(input_array[i][1])
    outputs = []

    # # Utilities
    motion_transformations_y_x = {
        "U": np.array([1, 0]),
        "D": np.array([-1, 0]),
        "L": np.array([0, -1]),
        "R": np.array([0, 1]),
    }

    # # Calculate grid size
    vertical_max_min = [0, 0]
    horizontal_max_min = [0, 0]
    grid_coords_y_x = [0, 0]
    for motion in input_array:
        grid_coords_y_x += motion_transformations_y_x[motion[0]] * motion[1]
        vertical_max_min[0] = max(vertical_max_min[0], grid_coords_y_x[0])
        vertical_max_min[1] = min(vertical_max_min[1], grid_coords_y_x[0])
        horizontal_max_min[0] = max(horizontal_max_min[0], grid_coords_y_x[1])
        horizontal_max_min[1] = min(horizontal_max_min[1], grid_coords_y_x[1])

    """
    # Notes
    - Grid size not given, need to calculate
        - Added code to account for negative index, just in case
            - Turned out not to be unnecessary
            - This paid off once I took a look at the full input, which had negative index
    - Head can travel max 2 units without tail moving (Part 1)
        - Tail will be directly behind head for movement distances of >= 3 units
        - (Part 2) 18 units for a 10-long rope
            - Can generalise to 2(n-1) units for a n-long rope
    - Understanding Part 2
        - Rope movement seems somewhat erratic at first, but not on closer inspection
        - Rope movement can be broken down into individual parts
            - Head is king: When `H` is detached from `1`, `1` goes directly behind `H`
            - Part-wise: More force = Move that direction
                - Applies to when `1` is detached from `2`, `2` from `3`, etc.
                - Let the part w/ the smaller number be the lead, and the other part the follower
                - Consider coord diff btw new_lead and follower
                    - new_lead is the new coords of the lead after it has moved this "turn"
                - Follower goes adjacent to lead in 1 of 3 ways:
                    - abs(x_coord_diff) > abs(y_coord_diff): Teleport to be either left or right of lead
                    - abs(x_coord_diff) < abs(y_coord_diff): Teleport to be either up or down from lead
                    - abs(x_coord_diff) = abs(y_coord_diff): Teleport to be diagonally adjacent to lead
                    - To decide which side to teleport to, just move in same general direction of lead
            - Note that rope parts can move in diagonals, while head cannot
    """

    # Part 1

    # # Generate grid (~~technically unnecessary, but also~~ accounts for negative index)
    has_visited_y_x = np.full(
        (
            len(range(*vertical_max_min[::-1])) + 1,
            len(range(*horizontal_max_min[::-1])) + 1,
        ),
        False,
    )
    head_coords_y_x = np.array([-vertical_max_min[1], -horizontal_max_min[1]])
    has_visited_y_x[tuple(head_coords_y_x)] = True

    # # Calculate tail positions
    tail_coords_y_x = head_coords_y_x.copy()
    for motion in input_array:
        for distance_moved in range(1, motion[1] + 1):
            old_head_coords_y_x = head_coords_y_x.copy()
            head_coords_y_x += motion_transformations_y_x[motion[0]]
            if np.all(np.isin(abs(head_coords_y_x - tail_coords_y_x), (0, 1))):
                # Tail is adjacent to head, don't move tail
                pass
            else:
                # Move rest of the distance required, tail is guaranteed to be directly behind head
                # Meant to be an optimisation instead of doing each and every step
                head_coords_y_x += motion_transformations_y_x[motion[0]] * (
                    motion[1] - distance_moved
                )
                tail_coords_y_x = (
                    head_coords_y_x.copy() - motion_transformations_y_x[motion[0]]
                )
                has_visited_y_x[
                    min(old_head_coords_y_x[0], tail_coords_y_x[0]) : max(
                        old_head_coords_y_x[0], tail_coords_y_x[0]
                    )
                    + 1,
                    min(old_head_coords_y_x[1], tail_coords_y_x[1]) : max(
                        old_head_coords_y_x[1], tail_coords_y_x[1]
                    )
                    + 1,
                ] = True
                break

    # # Count visited positions
    outputs.append(np.count_nonzero(has_visited_y_x))
    # outputs.append(np.sum(has_visited_y_x)) also works

    # Part 2

    # # Generate grid (accounts for negative index)
    has_visited_y_x = np.full(
        (
            len(range(*vertical_max_min[::-1])) + 1,
            len(range(*horizontal_max_min[::-1])) + 1,
        ),
        False,
    )
    rope_coords_y_x = np.array([[-vertical_max_min[1], -horizontal_max_min[1]]] * 10)
    has_visited_y_x[tuple(rope_coords_y_x[0])] = True

    # # Calculate tail positions
    for motion in input_array:
        for distance_moved in range(1, motion[1] + 1):
            # Move head
            rope_coords_y_x[0] += motion_transformations_y_x[motion[0]]

            # Adjust rest of rope accordingly
            for rope_part_num in range(10 - 1):
                if np.all(
                    np.isin(
                        abs(
                            rope_coords_y_x[rope_part_num]
                            - rope_coords_y_x[rope_part_num + 1]
                        ),
                        (0, 1),
                    )
                ):
                    # Lead rope part is adjacent to follower rope part, don't move follower
                    pass
                else:
                    # Shift follower rope part accordingly
                    y_coord_diff = (
                        rope_coords_y_x[rope_part_num][0]
                        - rope_coords_y_x[rope_part_num + 1][0]
                    )
                    x_coord_diff = (
                        rope_coords_y_x[rope_part_num][1]
                        - rope_coords_y_x[rope_part_num + 1][1]
                    )

                    if abs(y_coord_diff) > abs(x_coord_diff):
                        # Move vertically
                        if y_coord_diff > 0:
                            rope_coords_y_x[rope_part_num + 1] = rope_coords_y_x[
                                rope_part_num
                            ] + (-1, 0)
                        else:
                            rope_coords_y_x[rope_part_num + 1] = rope_coords_y_x[
                                rope_part_num
                            ] + (1, 0)

                    elif abs(y_coord_diff) < abs(x_coord_diff):
                        # Move horizontally
                        if x_coord_diff > 0:
                            rope_coords_y_x[rope_part_num + 1] = rope_coords_y_x[
                                rope_part_num
                            ] + (0, -1)
                        else:
                            rope_coords_y_x[rope_part_num + 1] = rope_coords_y_x[
                                rope_part_num
                            ] + (0, 1)

                    else:
                        # Move diagonally
                        # # Teleport vertically
                        if y_coord_diff > 0:
                            rope_coords_y_x[rope_part_num + 1] = rope_coords_y_x[
                                rope_part_num
                            ] + (-1, 0)
                        else:
                            rope_coords_y_x[rope_part_num + 1] = rope_coords_y_x[
                                rope_part_num
                            ] + (1, 0)
                        # # Adjust horizontally
                        if x_coord_diff > 0:
                            rope_coords_y_x[rope_part_num + 1] += (0, -1)
                        else:
                            rope_coords_y_x[rope_part_num + 1] += (0, 1)

            # Consider tail position
            has_visited_y_x[tuple(rope_coords_y_x[-1])] = True

    # # Count visited positions
    outputs.append(np.count_nonzero(has_visited_y_x))

    return outputs
