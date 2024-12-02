def run(input_str):
    # Initial setup
    input_array = [
        dict(
            map(
                lambda x: (x[0], int(x[1])),
                [j.split(": ") for j in i.split(": ", 1)[1].split(", ")],
            )
        )
        for i in input_str.split("\n")
    ]
    reference_data = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    outputs = []

    # Part 1
    for i, test_data in enumerate(input_array):
        try:
            for attribute in test_data.items():
                assert attribute in reference_data.items()
            outputs.append(i + 1)
            break
        except AssertionError:
            pass

    # Part 2
    for i, test_data in enumerate(input_array):
        try:
            for attribute in test_data.items():
                if attribute[0] in ("cats", "trees"):
                    assert attribute[1] > reference_data[attribute[0]]
                elif attribute[0] in ("pomeranians", "goldfish"):
                    assert attribute[1] < reference_data[attribute[0]]
                else:
                    assert attribute in reference_data.items()
            outputs.append(i + 1)
            break
        except AssertionError:
            pass

    return outputs
