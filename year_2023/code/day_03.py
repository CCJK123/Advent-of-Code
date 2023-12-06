def day_03(input_str):
    # Initial setup
    import re

    input_array = input_str.split("\n")
    outputs = []

    # Part 1
    part_no_sum = 0

    for row_no, row in enumerate(input_array):
        position = 0
        current_symbol = re.search(r"[^\d.]", row)

        while current_symbol is not None:
            position += current_symbol.span()[0]

            # Get number(s)
            ## Left
            part_no = re.search(r"\d+$", row[:position])
            if part_no is not None:
                part_no_sum += int(part_no.group())
            ## Right
            part_no = re.search(r"^\d+", row[position + 1 :])
            if part_no is not None:
                part_no_sum += int(part_no.group())

            ## Up & Down
            for modified_row_no in (row_no - 1, row_no + 1):
                if input_array[modified_row_no][position] == ".":
                    # Case 1: D.D, D.., ..D, or ... (between 0 to 2 matches)
                    left_part_no = re.search(
                        r"\d+$", input_array[modified_row_no][:position]
                    )
                    if left_part_no is not None:
                        part_no_sum += int(left_part_no.group())
                    right_part_no = re.search(
                        r"^\d+", input_array[modified_row_no][position + 1 :]
                    )
                    if right_part_no is not None:
                        part_no_sum += int(right_part_no.group())
                elif input_array[modified_row_no][position] in "0123456789":
                    # Case 2: .D., DD., .DD, or DDD (must have 1 match)
                    test_str = input_array[modified_row_no][position - 1 : position + 2]
                    if re.search(r"^\.\d\.$", test_str) is not None:
                        part_no = test_str[1]
                    elif re.search(r"^\d{2}\.$", test_str) is not None:
                        part_no = re.search(
                            r"\d+$", input_array[modified_row_no][: position + 1]
                        ).group()  # type: ignore
                    elif re.search(r"^\.\d{2}$", test_str) is not None:
                        part_no = re.search(
                            r"^\d+", input_array[modified_row_no][position:]
                        ).group()  # type: ignore
                    else:
                        part_no = test_str
                    part_no_sum += int(part_no)

            position += 1
            current_symbol = re.search(r"[^\d.]", row[position:])

    outputs.append(part_no_sum)

    # Part 2
    gear_ratio_sum = 0

    for row_no, row in enumerate(input_array):
        position = 0
        current_gear = re.search(r"\*", row)

        while current_gear is not None:
            position += current_gear.span()[0]
            part_no_list = []

            # Get number(s)
            ## Left
            part_no = re.search(r"\d+$", row[:position])
            if part_no is not None:
                part_no_list.append(int(part_no.group()))
            ## Right
            part_no = re.search(r"^\d+", row[position + 1 :])
            if part_no is not None:
                part_no_list.append(int(part_no.group()))

            ## Up & Down
            for modified_row_no in (row_no - 1, row_no + 1):
                if input_array[modified_row_no][position] == ".":
                    # Case 1: D.D, D.., ..D, or ... (between 0 to 2 matches)
                    left_part_no = re.search(
                        r"\d+$", input_array[modified_row_no][:position]
                    )
                    if left_part_no is not None:
                        part_no_list.append(int(left_part_no.group()))
                    right_part_no = re.search(
                        r"^\d+", input_array[modified_row_no][position + 1 :]
                    )
                    if right_part_no is not None:
                        part_no_list.append(int(right_part_no.group()))
                elif input_array[modified_row_no][position] in "0123456789":
                    # Case 2: .D., DD., .DD, or DDD (must have 1 match)
                    test_str = input_array[modified_row_no][position - 1 : position + 2]
                    if re.search(r"^\.\d\.$", test_str) is not None:
                        part_no = test_str[1]
                    elif re.search(r"^\d{2}\.$", test_str) is not None:
                        part_no = re.search(
                            r"\d+$", input_array[modified_row_no][: position + 1]
                        ).group()  # type: ignore
                    elif re.search(r"^\.\d{2}$", test_str) is not None:
                        part_no = re.search(
                            r"^\d+", input_array[modified_row_no][position:]
                        ).group()  # type: ignore
                    else:
                        part_no = test_str
                    part_no_list.append(int(part_no))

            # Get gear ratio, if exists
            if len(part_no_list) == 2:
                gear_ratio_sum += part_no_list[0] * part_no_list[1]

            position += 1
            current_gear = re.search(r"\*", row[position:])

    outputs.append(gear_ratio_sum)

    return outputs
