def day_10(input_str):
    # Initial setup
    import re
    def look_and_say(sequence, iterations_left):
        if iterations_left != 0:
            sequence_new = ""
            for match_obj in re.finditer(r"(\d)\1*", sequence):
                sequence_new += str(len(match_obj.group(0))) + match_obj.group(1)
            return look_and_say(sequence_new, iterations_left-1)
        else:
            return sequence
    outputs = []

    # Part 1
    sequence = look_and_say(input_str, 40)
    outputs.append(len(sequence))

    # Part 2
    sequence = look_and_say(sequence, 50-40)
    outputs.append(len(sequence))
   
    return outputs
