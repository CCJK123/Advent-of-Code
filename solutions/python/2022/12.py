def run(input_str):
    # Initial setup
    input_array = [list(i) for i in input_str.split("\n")]
    start = end = (None, None)
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if ord("a") <= ord(input_array[i][j]) <= ord("z"):
                input_array[i][j] = ord(input_array[i][j]) - ord("a") + 1
            elif input_array[i][j] == "S":
                start = (i, j)
                input_array[i][j] = 0
            elif input_array[i][j] == "E":
                end = (i, j)
                input_array[i][j] = 27

    import networkx as nx

    pathways = nx.DiGraph()
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            # Not top row
            if i != 0:
                if input_array[i][j] + 1 >= input_array[i - 1][j]:
                    pathways.add_edge((i, j), (i - 1, j))
            # Not bottom row
            if i != len(input_array) - 1:
                if input_array[i][j] + 1 >= input_array[i + 1][j]:
                    pathways.add_edge((i, j), (i + 1, j))
            # Not left column
            if j != 0:
                if input_array[i][j] + 1 >= input_array[i][j - 1]:
                    pathways.add_edge((i, j), (i, j - 1))
            # Not right column
            if j != len(input_array[i]) - 1:
                if input_array[i][j] + 1 >= input_array[i][j + 1]:
                    pathways.add_edge((i, j), (i, j + 1))

    outputs = []

    # Part 1
    outputs.append(nx.dijkstra_path_length(pathways, start, end))

    # Part 2
    min_path_length = None
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if input_array[i][j] <= 1:
                # Check if it's a viable starting point
                # (i.e. not all same height (`S` or `a`) or much taller (tall - short > 1))
                # (this was meant to be a time optimisation, realised later it wasn't rlly necessary)
                # (seems to give a roughly 55% time optimisation for the given input though)
                is_viable = [True] * 4

                # # Not top row
                if i != 0:
                    if (
                        input_array[i - 1][j] <= 1
                        or input_array[i - 1][j] - input_array[i][j] > 1
                    ):
                        is_viable[0] = False
                # # Not bottom row
                if i != len(input_array) - 1:
                    if (
                        input_array[i + 1][j] <= 1
                        or input_array[i + 1][j] - input_array[i][j] > 1
                    ):
                        is_viable[1] = False
                # # Not left column
                if j != 0:
                    if (
                        input_array[i][j - 1] <= 1
                        or input_array[i][j - 1] - input_array[i][j] > 1
                    ):
                        is_viable[2] = False
                # # Not right column
                if j != len(input_array[i]) - 1:
                    if (
                        input_array[i][j + 1] <= 1
                        or input_array[i][j + 1] - input_array[i][j] > 1
                    ):
                        is_viable[3] = False

                # Perform dijkstra if viable
                if True in is_viable:
                    try:
                        if min_path_length != None:
                            min_path_length = min(
                                min_path_length,
                                nx.dijkstra_path_length(pathways, (i, j), end),
                            )
                        else:
                            min_path_length = nx.dijkstra_path_length(
                                pathways, (i, j), end
                            )
                    except nx.NetworkXNoPath:
                        pass

    outputs.append(min_path_length)

    return outputs
