def run(input_str):
    # Initial Setup
    input_array = input_str.split(",")
    input_array = [int(i) for i in input_array]
    outputs = []

    # Part 1
    fishes = input_array.copy()
    for day in range(80):
        for i in range(len(fishes)):
            if fishes[i] == 0:
                fishes[i] = 6
                fishes.append(8)
            else:
                fishes[i] -= 1
    outputs.append(len(fishes))

    # Part 2
    fishes = input_array.copy()
    fish_age_counts = [0] * 9
    for i in fishes:
        fish_age_counts[i] += 1
    for day in range(256):
        fish_age_counts = fish_age_counts[1:9] + [fish_age_counts[0]]
        fish_age_counts[6] += fish_age_counts[8]
    total = 0
    for i in fish_age_counts:
        total += i
    outputs.append(total)

    return outputs
