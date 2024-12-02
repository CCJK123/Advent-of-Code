def run(input_str):
    # Initial setup
    import copy

    input_array = [i.split("\n  ") for i in input_str.split("\n\n")]
    for i in range(len(input_array)):
        input_array[i] = {
            "items": [int(j) for j in input_array[i][1][16:].split(", ")],
            "operation": input_array[i][2][11:]
            .replace("old", "new")
            .replace("new", "item_worry_level"),
            "test": [
                int(input_array[i][3][19:]),
                {
                    True: int(input_array[i][4][27:]),
                    False: int(input_array[i][5][28:]),
                },
            ],
        }
    outputs = []

    # Part 1
    inspection_counts = [0] * len(input_array)
    monkeys = copy.deepcopy(input_array)
    for rounds in range(20):
        for monkey_no in range(len(input_array)):
            for item_worry_level in monkeys[monkey_no]["items"]:
                # Inspection
                inspection_counts[monkey_no] += 1
                locals_copy = locals().copy()
                exec(monkeys[monkey_no]["operation"], globals(), locals_copy)
                item_worry_level = locals_copy["item_worry_level"]
                # Post inspection
                item_worry_level = int(item_worry_level / 3)
                # Test
                if item_worry_level % monkeys[monkey_no]["test"][0] == 0:
                    monkeys[monkeys[monkey_no]["test"][1][True]]["items"].append(
                        item_worry_level
                    )
                else:
                    monkeys[monkeys[monkey_no]["test"][1][False]]["items"].append(
                        item_worry_level
                    )
            # Clear items
            monkeys[monkey_no]["items"] = []

    inspection_counts.sort()
    outputs.append(inspection_counts[-1] * inspection_counts[-2])

    # Part 2
    inspection_counts = [0] * len(input_array)
    monkeys = copy.deepcopy(input_array)

    from math import lcm

    divisibility_tests_lcm = lcm(*[monkeys[i]["test"][0] for i in range(len(monkeys))])

    for rounds in range(10000):
        for monkey_no in range(len(input_array)):
            for item_worry_level in monkeys[monkey_no]["items"]:
                # Inspection
                inspection_counts[monkey_no] += 1
                locals_copy = locals().copy()
                exec(monkeys[monkey_no]["operation"], globals(), locals_copy)
                item_worry_level = locals_copy["item_worry_level"]
                # Post inspection (use divisibility tests' lcm for big number handling)
                item_worry_level = item_worry_level % divisibility_tests_lcm
                # Test
                if item_worry_level % monkeys[monkey_no]["test"][0] == 0:
                    monkeys[monkeys[monkey_no]["test"][1][True]]["items"].append(
                        item_worry_level
                    )
                else:
                    monkeys[monkeys[monkey_no]["test"][1][False]]["items"].append(
                        item_worry_level
                    )
            # Clear items
            monkeys[monkey_no]["items"] = []

    inspection_counts.sort()
    outputs.append(inspection_counts[-1] * inspection_counts[-2])

    return outputs
