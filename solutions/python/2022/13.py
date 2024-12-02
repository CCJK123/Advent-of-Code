def run(input_str):
    # Initial setup
    input_array = [i.split("\n") for i in input_str.split("\n\n")]
    outputs = []

    def check_correct_order(packet_pair):
        # Get left and right stacks
        locals_copy = locals().copy()
        exec(f"left_stack = {packet_pair[0]}", globals(), locals_copy)
        exec(f"right_stack = {packet_pair[1]}", globals(), locals_copy)
        left_stack = locals_copy["left_stack"]
        right_stack = locals_copy["right_stack"]

        # Setup for checks
        correct_order = None

        # Do checks
        count = 0
        while correct_order == None:
            # Prune equivalent values
            while left_stack != [] and right_stack != []:
                if left_stack[0] == right_stack[0]:
                    left_stack.pop(0)
                    right_stack.pop(0)
                else:
                    break

            # Switch for if either stack is empty
            if left_stack == [] and right_stack != []:
                correct_order = True
                break
            elif left_stack != [] and right_stack == []:
                correct_order = False
                break
            elif left_stack == [] and right_stack == []:
                break  # Both stacks empty (i.e. both stacks the same)

            # Switch for iff either value is "break"
            # (used to indicate hierarchy change for the "ran out of items" check)
            # (for when multiple layers of nesting is used)
            if left_stack[0] == "break" and right_stack[0] != "break":
                correct_order = True
                break
            elif left_stack[0] != "break" and right_stack[0] == "break":
                correct_order = False
                break

            # Switch for iff both values are lists
            if type(left_stack[0]) == type(right_stack[0]) == list:
                left_stack = left_stack[0] + ["break"] + left_stack[1:]
                right_stack = right_stack[0] + ["break"] + right_stack[1:]

            # Switch for iff both values are integers
            elif type(left_stack[0]) == type(right_stack[0]) == int:
                if left_stack[0] < right_stack[0]:
                    correct_order = True
                    break
                elif left_stack[0] > right_stack[0]:
                    correct_order = False
                    break

            # Switch for if values are of differing types
            elif type(left_stack[0]) == int and type(right_stack[0]) == list:
                left_stack[0] = [left_stack[0]]
            elif type(left_stack[0]) == list and type(right_stack[0]) == int:
                right_stack[0] = [right_stack[0]]

        # Return if stacks in correct order
        return correct_order

    # Part 1
    index_sum = 0
    for index, packet_pair in enumerate(input_array, 1):
        # Check if stacks in correct order
        correct_order = check_correct_order(packet_pair)

        # Add index to sum if in correct order
        if correct_order:
            index_sum += index

    outputs.append(index_sum)

    # Part 2
    packets = ["[[2]]", "[[6]]"]
    for packet_pair in input_array:
        packets += packet_pair

    from functools import cmp_to_key

    def packet_compare(right_stack, left_stack):
        correct_order = check_correct_order((left_stack, right_stack))
        if correct_order:
            return 1
        elif not correct_order:
            return -1
        else:
            return 0

    packets.sort(key=cmp_to_key(packet_compare))
    outputs.append((packets.index("[[2]]") + 1) * (packets.index("[[6]]") + 1))

    return outputs
