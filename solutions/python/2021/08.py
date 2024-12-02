def run(input_str):
    # Initial Setup
    input_array = input_str.split("\n")
    input_array = [
        [["".join(sorted(k)) for k in j.split(" ")] for j in i.split(" | ")]
        for i in input_array
    ]
    outputs = []

    # Part 1
    count = 0
    for i in input_array:
        for j in i[1]:
            if len(j) in (2, 3, 4, 7):
                count += 1
    outputs.append(count)

    # Part 2
    digits = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }
    # supposed seg -> actual seg
    seg_mappings = [{} for i in input_array]
    # num -> segs
    num_mappings = [{} for i in input_array]

    """
    deduce a by comparing 1(c,f, 2 long) and 7(a,c,f, 3 long)
    deduce f by seeing which no. does not have f
    deduce c by seeing what is not f in 1

    deduce g by seeing what the not 1/4/7 all have that is not a
    deduce e by seeing what 1/4/7 all do not have that is not g

    deduce d by seeing which 5 long has a,c,f,g (check for 3)

    deduce b by seeing what is not c,d,f in 4
    """

    total = 0
    for i in range(len(input_array)):
        patterns = input_array[i][0]

        # get num_mappings for 1, 4, 7, 8
        for pattern in patterns:
            if len(pattern) == 2:
                num_mappings[i][1] = pattern
            elif len(pattern) == 4:
                num_mappings[i][4] = pattern
            elif len(pattern) == 3:
                num_mappings[i][7] = pattern
            elif len(pattern) == 7:
                num_mappings[i][8] = pattern

        # deduce a
        seg_mappings[i]["a"] = num_mappings[i][7]
        for seg in num_mappings[i][1]:
            seg_mappings[i]["a"] = seg_mappings[i]["a"].replace(seg, "")

        # deduce f
        seg_counts = {}
        for seg in "abcdefg":
            seg_counts[seg] = 0
        for pattern in patterns:
            for seg in pattern:
                seg_counts[seg] += 1
        for seg in "abcdefg":
            if seg_counts[seg] == 9:
                seg_mappings[i]["f"] = seg

        # deduce c
        seg_mappings[i]["c"] = num_mappings[i][1].replace(seg_mappings[i]["f"], "")

        # deduce g
        common_not_147 = "abcdefg"
        for pattern in patterns:
            if len(pattern) not in (2, 3, 4):
                for seg in common_not_147:
                    if seg not in pattern:
                        common_not_147 = common_not_147.replace(seg, "")
        seg_mappings[i]["g"] = common_not_147.replace(seg_mappings[i]["a"], "")

        # deduce e
        missing_147 = "abcdefg"
        for num in (1, 4, 7):
            for segs in num_mappings[i][num]:
                for seg in segs:
                    if seg in missing_147:
                        missing_147 = missing_147.replace(seg, "")
        seg_mappings[i]["e"] = missing_147.replace(seg_mappings[i]["g"], "")

        # deduce d
        for pattern in patterns:
            if len(pattern) == 5:
                is3 = True
                for seg in "acfg":
                    if seg_mappings[i][seg] not in pattern:
                        is3 = False
                if is3 == True:
                    seg_mappings[i]["d"] = pattern
                    for seg in "acfg":
                        seg_mappings[i]["d"] = seg_mappings[i]["d"].replace(
                            seg_mappings[i][seg], ""
                        )

        # deduce b
        seg_mappings[i]["b"] = num_mappings[i][4]
        for seg in "cdf":
            seg_mappings[i]["b"] = seg_mappings[i]["b"].replace(
                seg_mappings[i][seg], ""
            )

        # convert 4 digit output patterns to a number
        seg_mappings[i] = {v: k for k, v in seg_mappings[i].items()}
        out_vals = input_array[i][1]
        for segs in out_vals:
            digit = ""
            for seg in segs:
                digit += seg_mappings[i][seg]
            digit = "".join(sorted(digit))
            digit = digits[digit]
            out_vals[out_vals.index(segs)] = digit
        total += int("".join(out_vals))
    outputs.append(total)

    return outputs
