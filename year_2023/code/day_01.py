def day_01(input_str):
    # Initial setup
    import re

    input_array = input_str.split("\n")
    outputs = []

    # Part 1
    num_array = input_array.copy()
    num_sum = 0

    for line in num_array:
        line = re.sub(r"[a-z]+", "", line)
        num_sum += int(line[0] + line[-1])

    outputs.append(num_sum)

    # Part 2
    num_array = input_array.copy()
    num_sum = 0
    numerical_words = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    for line in num_array:
        # Search for first numerical word
        original_line_length = len(line)
        buffer_length = 0
        while original_line_length == len(line):
            if re.search(rf"^\D{{{buffer_length}}}\d", line) != None:
                break
            for number in numerical_words.keys():
                line = re.sub(
                    rf"^\D{{{buffer_length}}}{number}", numerical_words[number], line
                )
            if buffer_length + 3 > len(line):
                break
            buffer_length += 1

        # Search for last numerical word
        original_line_length = len(line)
        buffer_length = 0
        while original_line_length == len(line):
            if re.search(rf"\d\D{{{buffer_length}}}$", line) != None:
                break
            for number in numerical_words.keys():
                line = re.sub(
                    rf"{number}\D{{{buffer_length}}}$", numerical_words[number], line
                )
            if buffer_length + 3 > len(line):
                break
            buffer_length += 1

        line = re.sub(r"[a-z]+", "", line)
        num_sum += int(line[0] + line[-1])

    outputs.append(num_sum)

    return outputs
