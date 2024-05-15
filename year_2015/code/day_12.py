def day_12(input_str):
    # Initial setup
    import json, re
    input_json = json.loads(input_str)
    outputs = []

    # Part 1
    num_sum = 0
    for match_obj in re.finditer(r"-?\d+", input_str):
        num_sum += int(match_obj.group(0))
    outputs.append(num_sum)

    # Part 2
    def parse(obj):
        match obj:
            case int():
                return obj
            case str():
                if obj == "red":
                    return None
                return 0
            case list():
                sub_num_sum = 0
                for sub_obj in obj:
                    temp = parse(sub_obj)
                    if temp is not None:
                        sub_num_sum += temp
                return sub_num_sum
            case dict():
                if "red" not in obj.values():
                    return parse(list(obj.values()))
                return 0
    outputs.append(parse(input_json))
    
    return outputs
