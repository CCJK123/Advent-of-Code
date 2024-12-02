def run(input_str):
    # Initial Setup
    input_array = input_str.split("\n")
    bracket_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    outputs = []

    # Part 1
    error_score = {")": 3, "]": 57, "}": 1197, ">": 25137}
    total_score = 0
    incomplete = input_array.copy()  # for part 2
    for line in input_array:
        stack = []
        for bracket in line:
            if bracket in bracket_pairs.keys():
                stack.append(bracket)
            elif bracket in bracket_pairs.values():
                last_open_bracket = stack.pop()
                if bracket != bracket_pairs[last_open_bracket]:
                    total_score += error_score[bracket]
                    incomplete.remove(line)  # for part 2
                    break
    outputs.append(total_score)

    # Part 2
    autocomp_score = {")": 1, "]": 2, "}": 3, ">": 4}
    total_scores = [0] * len(incomplete)
    for i in range(len(incomplete)):
        line = incomplete[i]
        stack = []
        for bracket in line:
            if bracket in bracket_pairs.keys():
                stack.append(bracket)
            elif bracket in bracket_pairs.values():
                _ = stack.pop()
        stack.reverse()
        for bracket in stack:
            total_scores[i] *= 5
            total_scores[i] += autocomp_score[bracket_pairs[bracket]]
    total_scores.sort()
    outputs.append(total_scores[int((len(incomplete) - 1) / 2)])

    return outputs
