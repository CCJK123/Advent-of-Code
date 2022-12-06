def day_03(input_str):
    # Initial setup
    input_array = input_str.split("\n")
    outputs = []

    def get_priority(item):
        priority = 0
        if ord("a") <= ord(item) <= ord("z"):
            priority += ord(item) - ord("a") + 1
        else:
            priority += ord(item) - ord("A") + 27
        return priority

    # Part 1
    priority_sum = 0
    rucksacks = [(i[0:int(len(i)/2)], i[-int(len(i)/2):]) for i in input_array]
    for rucksack in rucksacks:
        error = list(set(rucksack[0]).intersection(rucksack[1]))[0]
        priority_sum += get_priority(error)
    outputs.append(priority_sum)

    # Part 2
    priority_sum = 0
    for i in range(int(len(input_array)/3)):
        badge = list(set(input_array[i*3+0]
                         ).intersection(input_array[i*3+1], input_array[i*3+2])
                     )[0]
        priority_sum += get_priority(badge)
    outputs.append(priority_sum)

    return outputs
