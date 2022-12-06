def day_05(input_str):
    # Initial setup
    import copy
    input_array = [i.split("\n") for i in input_str.split("\n\n")]
    outputs = []
    # # Handle stacks
    stacks = []
    for i in range(len(input_array[0][-1].split())):
        stack = []
        for j in range(len(input_array[0])-1):
            stack.append(input_array[0][j][4*i+1])
        stack = [i for i in stack if i != " "]
        stack.reverse()
        stacks.append(stack)
    input_array[0] = stacks.copy()
    # # Handle moves
    for i in range(len(input_array[1])):
        move = input_array[1][i]
        move = [int(j) for j in move[5:].replace("from", "to").split(" to ")]
        input_array[1][i] = move

    # Part 1
    stacks = copy.deepcopy(input_array[0])
    for i in input_array[1]:
        for j in range(i[0]):
            stacks[i[2]-1].append(stacks[i[1]-1].pop())
    msg = ""
    for stack in stacks:
        msg += stack[-1]
    outputs.append(msg)

    # Part 2
    stacks = copy.deepcopy(input_array[0])
    for i in input_array[1]:
        stacks[i[2]-1] += stacks[i[1]-1][-i[0]:]
        stacks[i[1]-1] = stacks[i[1]-1][:-i[0]]
    msg = ""
    for stack in stacks:
        msg += stack[-1]
    outputs.append(msg)

    return outputs
