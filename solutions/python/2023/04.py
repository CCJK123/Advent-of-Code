def run(input_str):
    # Initial setup
    input_array = [
        [set(int(k) for k in j.split()) for j in i.split(": ")[1].split(" | ")]
        for i in input_str.split("\n")
    ]
    outputs = []

    # Part 1
    points = 0
    for card in input_array:
        matches = len(card[0].intersection(card[1]))
        if matches != 0:
            points += 2 ** (matches - 1)
    outputs.append(points)

    # Part 2
    card_count = [1] * len(input_array)
    for card_no, card in enumerate(input_array):
        matches = len(card[0].intersection(card[1]))
        if matches != 0:
            for i in range(matches):
                card_count[card_no + i + 1] += card_count[card_no]
    outputs.append(sum(card_count))

    return outputs
