def day_07(input_str):
    # Initial setup

    input_array = [i.split(" ") for i in input_str.split("\n")]
    outputs = []

    # Part 1
    def grade_card(card: list[str]) -> float:
        # Count labels
        label_count = {}
        for label in card[0]:
            if label not in label_count.keys():
                label_count[label] = 1
            else:
                label_count[label] += 1

        # Determine hand type
        score = None
        hand_sets = [
            [5],
            [4, 1],
            [3, 2],
            [3, 1, 1],
            [2, 2, 1],
            [2, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        label_count_count = list(label_count.values())
        label_count_count.sort(reverse=True)
        for index, hand_set in enumerate(hand_sets):
            if hand_set == label_count_count:
                score = index
                break
        assert type(score) == int

        # Modify score for tiebreaking
        modifier_sequence = "AKQJT98765432"
        offset = 0.01
        for count, label in enumerate(card[0], start=1):
            score += modifier_sequence.index(label) * (offset**count)

        return score

    cards = input_array.copy()
    cards.sort(reverse=True, key=grade_card)
    winnings = 0
    for rank, card in enumerate(cards, start=1):
        winnings += int(card[1]) * rank
    outputs.append(winnings)

    # Part 2
    def grade_card_revised(card: list[str]) -> float:
        # Count labels
        label_count = {}
        for label in card[0]:
            if label not in label_count.keys():
                label_count[label] = 1
            else:
                label_count[label] += 1

        # Determine hand type
        score = None
        hand_sets = [
            [5],
            [4, 1],
            [3, 2],
            [3, 1, 1],
            [2, 2, 1],
            [2, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        label_count_count = list(label_count.values())
        label_count_count.sort(reverse=True)

        if "J" in label_count.keys() and card[0] != "JJJJJ":
            offset = label_count["J"]
            label_count_count.remove(label_count["J"])
            label_count_count[0] += offset

        for index, hand_set in enumerate(hand_sets):
            if hand_set == label_count_count:
                score = index
                break
        assert type(score) == int

        # Modify score for tiebreaking
        modifier_sequence = "AKQT98765432J"
        offset = 0.01
        for count, label in enumerate(card[0], start=1):
            score += modifier_sequence.index(label) * (offset**count)

        return score

    cards = input_array.copy()
    cards.sort(reverse=True, key=grade_card_revised)
    winnings = 0
    for rank, card in enumerate(cards, start=1):
        winnings += int(card[1]) * rank
    outputs.append(winnings)

    return outputs
