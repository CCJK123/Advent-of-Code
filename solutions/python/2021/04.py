def run(input_str):
    # Initial Setup
    input_array = input_str.split("\n\n")

    sequence = input_array[0].split(",")
    for i in range(len(sequence)):
        sequence[i] = int(sequence[i])

    boards = input_array[1:]
    for i in range(len(boards)):
        boards[i] = boards[i].split("\n")
        for j in range(len(boards[i])):
            boards[i][j] = boards[i][j].split()
            for k in range(len(boards[i][j])):
                boards[i][j][k] = int(boards[i][j][k])

    def check_bingo(board):
        bingo = False
        # Check rows
        for row in range(len(board)):
            if board[row].count("x") == 5:
                bingo = True
        # Check columns
        for column in range(len(board[row])):
            count = 0
            for row in range(len(board)):
                if board[row][column] == "x":
                    count += 1
            if count == 5:
                bingo = True
        return bingo

    outputs = []

    # Part 1
    mod_boards = boards.copy()

    for i in range(len(sequence)):
        for board in mod_boards:
            # Remove drawn values
            for row in range(len(board)):
                for column in range(len(board[row])):
                    if board[row][column] == sequence[i]:
                        board[row][column] = "x"
            if check_bingo(board):
                break
        if check_bingo(board):
            break

    unmarked_sum = 0
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] != "x":
                unmarked_sum += board[row][column]
    outputs.append(unmarked_sum * sequence[i])

    # Part 2
    mod_boards = boards.copy()
    pending_boards = list(range(len(boards)))
    last_board = None

    for i in range(len(sequence)):
        for j in range(len(mod_boards)):
            # Remove drawn values
            for row in range(len(mod_boards[j])):
                for column in range(len(mod_boards[j][row])):
                    if mod_boards[j][row][column] == sequence[i]:
                        mod_boards[j][row][column] = "x"
            if check_bingo(mod_boards[j]):
                if j in pending_boards:
                    pending_boards.remove(j)
            if len(pending_boards) == 1:
                last_board = pending_boards[0]
            elif len(pending_boards) == 0:
                break
        if len(pending_boards) == 0:
            break

    unmarked_sum = 0
    board = mod_boards[last_board]
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] != "x":
                unmarked_sum += board[row][column]
    outputs.append(unmarked_sum * sequence[i])

    return outputs
