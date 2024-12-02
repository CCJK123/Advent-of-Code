def run(input_str):
    # Initial setup
    input_array = [i.split("\n") for i in input_str.split("\n\n")]
    input_array[0] = [int(i) for i in input_array[0][0].split(" ")[1:]]
    for i in range(1, len(input_array)):
        input_array[i] = [[int(k) for k in j.split(" ")] for j in input_array[i][1:]]
    outputs = []

    # Part 1
    location_list = []
    for seed in input_array[0]:
        current_location = seed
        for stage in input_array[1:]:
            for destination, source, length in stage:
                if source <= current_location <= source + length - 1:
                    current_location = destination + (current_location - source)
                    break
        location_list.append(current_location)

    outputs.append(min(location_list))

    # Part 2
    ## Get min/max values of seed ranges
    seed_ranges = []
    for i in range(0, len(input_array[0]), 2):
        seed_ranges.append(
            (input_array[0][i], input_array[0][i] + input_array[0][i + 1] - 1)
        )

    ## Implement utility function
    def determine_set_relation(
        test_range: tuple[int, int], whole_range: tuple[int, int]
    ) -> dict[str, tuple[int, int] | list[tuple[int, int]] | None]:
        if whole_range[0] <= test_range[0] and whole_range[1] >= test_range[1]:
            # Case 1: Subset
            return {"overlap": test_range, "excess": None}
        elif whole_range[0] > test_range[0] and whole_range[1] < test_range[1]:
            # Case 2: Inverse Proper Subset
            return {
                "overlap": whole_range,
                "excess": [
                    (test_range[0], whole_range[0] - 1),
                    (whole_range[1] + 1, test_range[1]),
                ],
            }
        elif (
            whole_range[0] <= test_range[0]
            and test_range[0] < whole_range[1] < test_range[1]
        ):
            # Case 3: Partial Overlap (Left of Test Range)
            return {
                "overlap": (test_range[0], whole_range[1]),
                "excess": [(whole_range[1] + 1, test_range[1])],
            }
        elif (
            test_range[0] < whole_range[0] < test_range[1]
            and whole_range[1] >= test_range[1]
        ):
            # Case 4: Partial Overlap (Right of Test Range)
            return {
                "overlap": (whole_range[0], test_range[1]),
                "excess": [(test_range[0], whole_range[0] - 1)],
            }
        else:
            # Case 5: No Overlap
            return {"overlap": None, "excess": test_range}

    ## Collapse ranges
    location_range_min_list = []
    current_ranges = seed_ranges
    subsequent_ranges = []
    for stage in input_array[1:]:
        while current_ranges != []:
            has_overlap = False
            current_range = current_ranges[0]
            for destination, source, length in stage:
                set_relation = determine_set_relation(
                    current_range, (source, source + length - 1)
                )
                if set_relation["overlap"] is not None:
                    has_overlap = True
                    subsequent_ranges.append(
                        (
                            destination + (set_relation["overlap"][0] - source),
                            destination + (set_relation["overlap"][1] - source),
                        )
                    )
                    if set_relation["excess"] is not None:
                        current_ranges += set_relation["excess"]
                    break
            if has_overlap == False:
                subsequent_ranges.append(current_range)
            del current_ranges[0]
        current_ranges = subsequent_ranges
        subsequent_ranges = []

    outputs.append(min([i[0] for i in current_ranges]))

    return outputs
