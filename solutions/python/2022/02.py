def run(input_str):
    # Initial setup
    input_array = [i.split(" ") for i in input_str.split("\n")]
    outputs = []

    # Part 1
    total_score = 0
    shape_score = {"X": 1, "Y": 2, "Z": 3}
    win_pairs = {"X": "C", "Y": "A", "Z": "B"}
    for i in input_array:
        # Add to total score based on shape played
        total_score += shape_score[i[1]]
        # Add to total score based on game outcome
        if i[0] == win_pairs[i[1]]:
            total_score += 6  # Win
        elif ord(i[1]) - ord(i[0]) == 23:
            total_score += 3  # Draw
        else:
            total_score += 0  # Lose
    outputs.append(total_score)

    # Part 2
    total_score = 0
    shape_score = {"A": 1, "B": 2, "C": 3}
    win_pairs = {"A": "C", "B": "A", "C": "B"}
    lose_pairs = {"C": "A", "A": "B", "B": "C"}
    for i in input_array:
        if i[1] == "X":  # Lose
            total_score += 0 + shape_score[win_pairs[i[0]]]
        elif i[1] == "Y":  # Draw
            total_score += 3 + shape_score[i[0]]
        else:  # Win
            total_score += 6 + shape_score[lose_pairs[i[0]]]
    outputs.append(total_score)

    return outputs
