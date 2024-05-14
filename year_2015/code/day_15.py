def day_15(input_str):
    """My implementation seems quite inefficient, but hey it works"""

    # Initial setup
    import itertools, re
    input_array = []
    for match in re.finditer(r"([^ ]+):.+?(-*\d+).+?(-*\d+).+?(-*\d+).+?(-*\d+).+?(-*\d+)\n*", input_str):
        temp = [match.group(i) for i in range(1, 7)]
        for i in range(1, 6):
            temp[i] = int(temp[i])
        input_array.append(temp)
    outputs = []

    # Parts 1 & 2 Combined
    max_score = max_score_calories = 0
    for ingredient_amts in (i for i in itertools.product(range(101), repeat=len(input_array)) if sum(i)==100):
        score = 1
        for metric_index in range(1, 5):
            score *= max(0, sum((ingredient_amts[i]*input_array[i][metric_index] for i in range(len(input_array)))))
        # Part 1
        max_score = max(score, max_score)
        # Part 2
        if sum((ingredient_amts[i]*input_array[i][5] for i in range(len(input_array)))) == 500:
            max_score_calories = max(score, max_score_calories)
    outputs.extend([max_score, max_score_calories])

    return outputs
