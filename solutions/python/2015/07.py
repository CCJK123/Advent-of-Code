def run(input_str):
    # Initial setup
    import string

    input_array = [i.split(" -> ") for i in input_str.split("\n")]
    for i, instruction in enumerate(input_array):
        head = instruction[0].split(" ")
        if len(head) == 1:
            head = ["LIT"] + head
        elif len(head) == 3:
            head = [head.pop(1)] + head
        for j, parameter in enumerate(head[1:], 1):
            try:
                head[j] = int(parameter)
            except:
                pass
        input_array[i][0] = head

    def parse(wires, possible_wire):
        if type(possible_wire) == str:
            return wires[possible_wire]
        return possible_wire

    def propogate(wires, instructions):
        while instructions != []:
            instruction = instructions[0]
            try:
                if instruction[1] not in wires.keys():
                    match instruction[0][0]:
                        case "LIT":
                            wires[instruction[1]] = parse(wires, instruction[0][1])
                        case "NOT":
                            wires[instruction[1]] = ~parse(wires, instruction[0][1])
                        case "AND":
                            wires[instruction[1]] = parse(
                                wires, instruction[0][1]
                            ) & parse(wires, instruction[0][2])
                        case "OR":
                            wires[instruction[1]] = parse(
                                wires, instruction[0][1]
                            ) | parse(wires, instruction[0][2])
                        case "LSHIFT":
                            wires[instruction[1]] = (
                                parse(wires, instruction[0][1]) << instruction[0][2]
                            )
                        case "RSHIFT":
                            wires[instruction[1]] = (
                                parse(wires, instruction[0][1]) >> instruction[0][2]
                            )
            except KeyError:
                instructions.append(instruction)
            finally:
                del instructions[0]

        for key, value in wires.items():
            if value < 0:
                wires[key] += 65536

        return wires

    outputs = []

    # Part 1
    wires = propogate({}, input_array.copy())
    outputs.append(wires["a"])

    # Part 2
    wires = propogate({"b": wires["a"]}, input_array.copy())
    outputs.append(wires["a"])

    return outputs
