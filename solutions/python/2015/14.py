def run(input_str):
    # Initial setup
    import re

    input_array = []
    for match in re.finditer(r"\b([^ ]+).+?(\d+).+?(\d+).+?(\d+).+", input_str):
        temp = [match.group(i) for i in range(1, 5)]
        for i in range(1, 4):
            temp[i] = int(temp[i])
        input_array.append(temp)
    duration, outputs = 2503, []

    # Part 1
    distances = {}
    for data in input_array:
        distances[data[0]] = data[1] * (
            data[2] * (duration // (data[2] + data[3]))
            + min(data[2], duration % (data[2] + data[3]))
        )
    outputs.append(max(distances.values()))

    # Part 2
    distances, points = {}, {}
    for data in input_array:
        distances[data[0]] = points[data[0]] = 0
    for timestep in range(duration):
        for data in input_array:
            distances[data[0]] += (
                data[1] if (timestep % (data[2] + data[3]) < data[2]) else 0
            )
        for name in [
            name
            for name, distance in distances.items()
            if distance == max(distances.values())
        ]:
            points[name] += 1
    outputs.append(max(points.values()))

    return outputs
