def day_09(input_str):
    # Initial setup
    import numpy as np
    input_array = [i.split() for i in input_str.split("\n")]
    for i in range(len(input_array)):
        input_array[i][1] = int(input_array[i][1])

    motion_transformations_y_x = {
        "U": np.array([1, 0]),
        "D": np.array([-1, 0]),
        "L": np.array([0, -1]),
        "R": np.array([0, 1])
    }

    outputs = []

    '''
    # Notes
    - Grid size not given, need to calculate
        - Added code to account for negative index, just in case
            - Turned out not to be unnecessary
            - This paid off once I took a look at the full input, which had negative index
    - Head can travel max 2 units without tail moving (Part 1)
        - Tail will be directly behind head for movement distances of >= 3 units
        - (Part 2) 18 units for a 10-long rope
            - Can generalise to 2(n-1) units for a n-long rope
    '''

    # Part 1

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

    # # Generate grid (~~technically unnecessary, but also~~ accounts for negative index)
    has_visited_y_x = np.full(
        (len(range(*vertical_max_min[::-1]))+1, len(range(*horizontal_max_min[::-1]))+1), False)
    head_coords_y_x = np.array([-vertical_max_min[1], -horizontal_max_min[1]])
    has_visited_y_x[tuple(head_coords_y_x)] = True

    # # Calculate tail positions
    tail_coords_y_x = head_coords_y_x.copy()
    for motion in input_array:
        for distance_moved in range(1, motion[1]+1):
            old_head_coords_y_x = head_coords_y_x.copy()
            head_coords_y_x += motion_transformations_y_x[motion[0]]
            if np.all(np.isin(abs(head_coords_y_x-tail_coords_y_x), (0, 1))):
                # Tail is adjacent to head, don't move tail
                pass
            else:
                # Move rest of the distance required, tail is guaranteed to be directly behind head
                # Meant to be an optimisation instead of doing each and every step
                head_coords_y_x += motion_transformations_y_x[motion[0]] * \
                    (motion[1] - distance_moved)
                tail_coords_y_x = \
                    head_coords_y_x.copy() - \
                    motion_transformations_y_x[motion[0]]
                has_visited_y_x[
                    min(old_head_coords_y_x[0], tail_coords_y_x[0]): max(old_head_coords_y_x[0], tail_coords_y_x[0])+1,
                    min(old_head_coords_y_x[1], tail_coords_y_x[1]): max(old_head_coords_y_x[1], tail_coords_y_x[1])+1
                ] = True
                break

    # # Count visited positions
    outputs.append(np.count_nonzero(has_visited_y_x))
    # outputs.append(np.sum(has_visited_y_x)) also works

    return outputs
