def day_04(input_str):
    # Initial setup
    import hashlib
    outputs = []

    # Part 1
    number = 0
    while True:
        number += 1
        md5_hash = hashlib.md5(f"{input_str}{str(number)}".encode()).hexdigest()
        if md5_hash[:5] == "00000":
            break
    outputs.append(number)

    # Part 2
    while True:
        number += 1
        md5_hash = hashlib.md5(f"{input_str}{str(number)}".encode()).hexdigest()
        if md5_hash[:6] == "000000":
            break
    outputs.append(number)

    return outputs
