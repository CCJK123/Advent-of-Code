def day_06(input_str):
    # Initial setup
    input_array = [i.split()[1:] for i in input_str.split("\n")]
    outputs = []

    # Part 1
    output = 1
    races = []
    for i in range(len(input_array[0])):
        races.append((int(input_array[0][i]), int(input_array[1][i])))
    for time, distance_record in races:
        no_of_ways = 0
        for hold_time in range(1, time):
            if hold_time * (time - hold_time) > distance_record:
                no_of_ways += 1
        output *= no_of_ways
    outputs.append(output)

    # Part 2
    time, distance_record = (int("".join(i)) for i in input_array)
    hold_time_range = []
    for search in ((1, time, 1), (time, 1, -1)):
        for hold_time in range(*search):
            if hold_time * (time - hold_time) > distance_record:
                hold_time_range.append(hold_time)
                break
    outputs.append(hold_time_range[1] - hold_time_range[0] + 1)

    return outputs
