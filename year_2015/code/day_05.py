def day_05(input_str):
    # Initial setup
    import re, string
    input_array = input_str.split("\n")
    outputs = []

    # Part 1
    count = 0
    for test_string in input_array:
        try:
            vowel_count = 0
            for vowel in "aeiou":
                vowel_count += test_string.count(vowel)
            assert vowel_count >= 3

            has_double = False
            for char in string.ascii_lowercase:
                if char*2 in test_string:
                    has_double = True
            assert has_double == True
            
            for substring in ("ab", "cd", "pq", "xy"):
                assert substring not in test_string
            count += 1

        except:
            pass

    outputs.append(count)
    
    # Part 2
    count = 0
    for test_string in input_array:
        try:
            for regexp in (r"(..).*\1", r"(.).\1"):
                assert re.search(regexp, test_string) is not None
            count += 1
        except:
            pass
    outputs.append(count)

    return outputs
