def day_02(input_str):
    # Initial setup
    input_array = [
        [
            [(int(k.split(" ")[0]), k.split(" ")[1]) for k in j.split(", ")]
            for j in i.split(": ")[1].split("; ")
        ]
        for i in input_str.split("\n")
    ]
    outputs = []

    # Part 1
    id_sum = 0
    max_cube_amt = {"red": 12, "green": 13, "blue": 14}

    for id, game in enumerate(input_array, start=1):
        is_possible = True
        for cube_set in game:
            for info in cube_set:
                if info[0] > max_cube_amt[info[1]]:
                    is_possible = False
        if is_possible:
            id_sum += id
    outputs.append(id_sum)

    # Part 2
    power_sum = 0
    for game in input_array:
        min_cube_count = {"red": 0, "green": 0, "blue": 0}
        for cube_set in game:
            for info in cube_set:
                min_cube_count[info[1]] = max(min_cube_count[info[1]], info[0])
        power_sum += (
            min_cube_count["red"] * min_cube_count["green"] * min_cube_count["blue"]
        )
    outputs.append(power_sum)

    return outputs
