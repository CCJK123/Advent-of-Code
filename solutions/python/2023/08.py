def run(input_str):
    # Initial setup
    import math

    input_array = [i.split("\n") for i in input_str.split("\n\n")]
    input_array[0] = input_array[0][0]
    _ = {}
    for i, node in enumerate(input_array[1]):
        _[input_array[1][i][0:3]] = [input_array[1][i][7:10], input_array[1][i][12:15]]
    input_array[1] = _

    instruction_index = ["L", "R"]
    outputs = []

    # Part 1
    steps = 0
    current_node = "AAA"

    while current_node != "ZZZ":
        for instruction in input_array[0]:
            current_node = input_array[1][current_node][
                instruction_index.index(instruction)
            ]
            steps += 1

    outputs.append(steps)

    # Part 2
    """
    Some Comments
      - Originally tried brute-force solution to no avail, when it said it took
        "significantly more steps" I didn't expect the number of steps to be as big as
        it was, which ended up being over triple the order of magnitude of the part 1 
        solution lol
      - Working solution assumes all "Z" nodes cycle back to themselves after a certain
        number of steps, and reaching said "Z" node from its respective "A" node also
        takes the same number of steps as before, something which I'm pretty sure is not
        necessarily true for some random graph
      - However, I'm pretty sure the graph and movement instructions was generated in a 
        way such that this relationship holds true, although it wasn't explicitly stated
        in the problem statement
      - Hence, if we assume that each starting node becomes a "Z" node after every n
        steps (with n varying between the nodes), it allows us to get the overall number
        of steps required by considering the lowest common multiple of these values of n
         
    """

    starting_nodes = {(i if i[2] == "A" else None) for i in input_array[1].keys()}
    starting_nodes.remove(None)
    steps_list = []

    for node in starting_nodes:
        steps = 0
        current_node = node

        assert type(current_node) == str
        while current_node[2] != "Z":
            for instruction in input_array[0]:
                current_node = input_array[1][current_node][
                    instruction_index.index(instruction)
                ]
                steps += 1
        steps_list.append(steps)

    outputs.append(math.lcm(*steps_list))  # Assumes cyclic node relation

    return outputs
