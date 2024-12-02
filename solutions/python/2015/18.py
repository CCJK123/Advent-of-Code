def run(input_str):
    # Initial setup
    import copy, itertools

    input_array = input_str.split("\n")

    def setup_grid():
        grid_now = [
            [None] * (len(input_array[0]) + 2) for i in range(len(input_array) + 2)
        ]
        for row_no, row in enumerate(input_array, 1):
            for col_no, light in enumerate(row, 1):
                if light == "#":
                    grid_now[row_no][col_no] = True
                else:
                    grid_now[row_no][col_no] = False
        return grid_now

    def get_next_grid(grid_now):
        grid_next = copy.deepcopy(grid_now)
        for row_no, row in enumerate(grid_now[1:-1], 1):
            for col_no, light in enumerate(row[1:-1], 1):
                neighbours = []
                for offset in itertools.product((-1, 0, 1), repeat=2):
                    if offset != (0, 0):
                        neighbours.append(
                            grid_now[row_no + offset[0]][col_no + offset[1]]
                        )
                if light == True and not 2 <= neighbours.count(True) <= 3:
                    grid_next[row_no][col_no] = False
                elif light == False and neighbours.count(True) == 3:
                    grid_next[row_no][col_no] = True
        return grid_next

    outputs = []

    # Part 1
    grid_now = setup_grid()
    for step in range(100):
        grid_now = get_next_grid(grid_now)
    outputs.append(sum(row.count(True) for row in grid_now))

    # Part 2
    grid_now = setup_grid()

    def on_corners(grid):
        for row_no, col_no in itertools.product(
            (1, len(input_array)), (1, len(input_array[0]))
        ):
            grid[row_no][col_no] = True
        return grid

    for step in range(100):
        grid_now = get_next_grid(on_corners(grid_now))
    outputs.append(sum(row.count(True) for row in on_corners(grid_now)))

    return outputs
