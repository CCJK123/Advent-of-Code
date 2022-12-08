def day_08(input_str):
    # Initial setup
    import copy
    input_array = [[int(j) for j in list(i)] for i in input_str.split("\n")]
    outputs = []

    # Part 1
    count = 2*(len(input_array) + len(input_array[0])) - 4
    transposed_input_array = copy.deepcopy(input_array)
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            transposed_input_array[j][i] = input_array[i][j]

    for i in range(1, len(input_array)-1):
        for j in range(1, len(input_array[i])-1):
            is_visible = [True]*4
            # Top
            for k in transposed_input_array[j][:i]:
                if k >= input_array[i][j]:
                    is_visible[0] = False
            # Bottom
            for k in transposed_input_array[j][i+1:]:
                if k >= input_array[i][j]:
                    is_visible[1] = False
            # Left
            for k in input_array[i][:j]:
                if k >= input_array[i][j]:
                    is_visible[2] = False
            # Right
            for k in input_array[i][j+1:]:
                if k >= input_array[i][j]:
                    is_visible[3] = False
            # Check if visible from any
            if True in is_visible:
                count += 1

    outputs.append(count)

    # Part 2
    scenic_score_array = [[0]*len(input_array[0])
                          for i in range(len(input_array))]

    for i in range(1, len(input_array)-1):          # Can ignore edge trees since their
        for j in range(1, len(input_array[i])-1):   # scenic score will be 0
            scenic_score = [0]*4
            # Up
            for k in transposed_input_array[j][:i][::-1]:
                scenic_score[0] += 1
                if k >= input_array[i][j]:
                    break
            # Down
            for k in transposed_input_array[j][i+1:]:
                scenic_score[1] += 1
                if k >= input_array[i][j]:
                    break
            # Left
            for k in input_array[i][:j][::-1]:
                scenic_score[2] += 1
                if k >= input_array[i][j]:
                    break
            # Right
            for k in input_array[i][j+1:]:
                scenic_score[3] += 1
                if k >= input_array[i][j]:
                    break
            # Calculate scenic score
            scenic_score_array[i][j] = 1
            for k in range(4):
                scenic_score_array[i][j] *= scenic_score[k]

    outputs.append(max([max(i) for i in scenic_score_array]))

    return outputs
