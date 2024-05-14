def day_13(input_str):
    """Quite similar to AoC 2015 Day 9"""

    # Initial setup
    import itertools
    input_array = [
        i.replace("would ","").replace("lose ","-").replace("gain ","")
        .replace("happiness units by sitting next to ","").replace(".","")
        .split(" ")
        for i in input_str.split("\n")
    ]
    input_dict = {}
    for i in input_array:
        input_dict[(i[0], i[2])] = int(i[1])
    
    def calc_max_happiness(people, relationships):
        max_happiness = None
        for possible_seating in itertools.permutations(people, len(people)):
            happiness, possible_seating = 0, tuple(list(possible_seating) + [possible_seating[0]])
            for i in range(len(possible_seating)-1):
                for pair in itertools.permutations(tuple(possible_seating[i:i+2]), 2):
                    happiness += relationships[pair]
            if max_happiness is not None:
                if max_happiness < happiness:
                    max_happiness = happiness
            else:
                max_happiness = happiness
        return max_happiness
    
    outputs = []

    # Port 1
    people = set()
    for pair in input_dict.keys():
        people = people.union(pair)
    relationships = input_dict.copy()
    outputs.append(calc_max_happiness(people, relationships))

    # Part 2
    people.add("Self")
    for person in people:
        for pair in itertools.permutations(("Self", person), 2):
            relationships[pair] = 0
    outputs.append(calc_max_happiness(people, relationships))

    return outputs
