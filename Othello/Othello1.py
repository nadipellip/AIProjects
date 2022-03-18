import sys
OPTIONS = ("X", "O")
def setLookups(inputval):
    global HEIGHT, WIDTH, SIZE, BOARD,TURN,MOVES, ACTIVE,ACT
    ACTIVE = True
    ACT = True
    HEIGHT = 8
    WIDTH = 8
    SIZE = HEIGHT * WIDTH
    BOARD = ["." for i in range(SIZE)]
    BOARD[27], BOARD[28] = "O", "X"
    BOARD[35], BOARD[36] = "X", "O"
    BOARD = "".join(BOARD)
    BOARD = BOARD.upper()
    TURN = 0
    MOVES = []
    for val in inputval:
        if len(val) == 64:
            BOARD = val.upper()
        if val == "X" or val == "x":
            ACT = False
            TURN = 0
        if val == "O" or val == "o":
            ACT = False
            TURN = 1
        else:
            MOVES.append(val)
def playmove(pos):
    global HEIGHT, WIDTH, SIZE, BOARD,TURN,MOVES
    switch = {pos}
    p = 1
    s = set()
    while (pos // WIDTH) == ((pos+p) // WIDTH):
        if BOARD[pos + p] == OPTIONS[1-TURN]:
            s.add(pos + p)
            p+= 1
        elif BOARD[pos+p] == OPTIONS[TURN]:
            switch.add(s)
            break
        else:
            break
    p = 1
    s = set()
    while (pos // WIDTH) == ((pos - p) // WIDTH):
        if BOARD[pos - p] == OPTIONS[1 - TURN]:
            s.add(pos - p)
            p += 1
        elif BOARD[pos - p] == OPTIONS[TURN]:
            switch.add(s)
            break
        else:
            break
    p = 1
    s = set()
    while pos + p * WIDTH < SIZE:
        if BOARD[pos + p*WIDTH] == OPTIONS[1-TURN]:
            s.add(pos+p*WIDTH)
            p+= 1
        elif BOARD[pos + p*WIDTH] == OPTIONS[TURN]:
            print()
        else:
            break

    p = 1
    while pos - p*WIDTH >= 0:
        if BOARD[pos - p*WIDTH] == OPTIONS[1-TURN]:
            BOARD[pos-p*WIDTH] = OPTIONS[TURN]
            p+= 1
        else:
            break
    p = 1
    while (pos // WIDTH) == ((pos+p) // WIDTH) and pos+p*WIDTH+p < SIZE:
        if BOARD[pos +p * WIDTH + p ] == OPTIONS[1 - TURN]:
            BOARD[pos + p * WIDTH + p] = OPTIONS[TURN]
            p += 1
        else:
            break
    while (pos // WIDTH) == ((pos-p) // WIDTH) and pos+p*WIDTH-p < SIZE:
        if BOARD[pos +p * WIDTH - p ] == OPTIONS[1 - TURN]:
            BOARD[pos + p * WIDTH - p] = OPTIONS[TURN]
            p += 1
        else:
            break
    while (pos // WIDTH) == ((pos+p) // WIDTH) and pos-p*WIDTH+p > 0:
        if BOARD[pos -p * WIDTH + p ] == OPTIONS[1 - TURN]:
            BOARD[pos - p * WIDTH + p] = OPTIONS[TURN]
            p += 1
        else:
            break
    while (pos // WIDTH) == ((pos-p) // WIDTH) and pos-p*WIDTH-p >= 0:
        if BOARD[pos +p * WIDTH + p ] == OPTIONS[1 - TURN]:
            BOARD[pos + p * WIDTH + p] = OPTIONS[TURN]
            p += 1
        else:
            break
    TURN = 1 - TURN
def posmoves(board):
    if ACT:
        turn = board.count(".")%2
        letter = OPTIONS[turn]
    else:
        turn = TURN
        letter = OPTIONS[turn]
    moves = set()
    counter = 1
    for row in range(HEIGHT):
        for col in range(WIDTH):
            pos = row*WIDTH+col
            if board[pos] == letter:
                if (pos+1)//WIDTH == row and board[pos+1] == OPTIONS[1-turn]:
                    while (pos+counter) // WIDTH == row and board[pos+counter] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos+counter) // WIDTH == row and board[pos+counter] == ".":
                        moves.add(pos+counter)
                    counter = 1
                if (pos-1)//WIDTH == row and board[pos-1] == OPTIONS[1-turn]:
                    while (pos-counter) // WIDTH == row and board[pos-counter] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos-counter) // WIDTH == row and board[pos-counter] == ".":
                        moves.add(pos-counter)
                    counter = 1
                if (pos+WIDTH) < SIZE and board[pos+WIDTH] == OPTIONS[1-turn]:
                    while (pos+counter*WIDTH) < SIZE and board[pos+counter*WIDTH] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos+counter*WIDTH) < SIZE and board[pos+counter*WIDTH] == ".":
                        moves.add(pos+counter*WIDTH)
                    counter = 1
                if (pos-WIDTH) >= 0 and board[pos-WIDTH] == OPTIONS[1-turn]:
                    while (pos-counter*WIDTH) >= 0 and board[pos-counter*WIDTH] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos-counter*WIDTH) >= 0 and board[pos-counter*WIDTH] == ".":
                        moves.add(pos-counter*WIDTH)
                    counter = 1
                if (pos+WIDTH+1) < SIZE and (pos+WIDTH+1) // WIDTH == row + 1 and board[pos+WIDTH+1] == OPTIONS[1-turn]:
                    while (pos+counter*WIDTH + counter) < SIZE and (pos+WIDTH*counter+counter) // WIDTH == row+counter and board[pos+counter*WIDTH+counter] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos+counter*WIDTH+counter) < SIZE and (pos+WIDTH*counter+counter) // WIDTH == row + counter and board[pos+counter*WIDTH+counter] == ".":
                        moves.add(pos+counter*WIDTH + counter)
                    counter = 1
                if (pos+WIDTH-1) < SIZE and (pos+WIDTH-1) // WIDTH == row + 1 and board[pos+WIDTH-1] == OPTIONS[1-turn]:
                    while (pos+counter*WIDTH - counter) < SIZE and (pos+WIDTH*counter-counter) // WIDTH == row + counter and board[pos+counter*WIDTH-counter] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos+counter*WIDTH-counter) < SIZE and (pos+WIDTH*counter-counter) // WIDTH == row + counter and board[pos+counter*WIDTH-counter] == ".":
                        moves.add(pos+counter*WIDTH - counter)
                    counter = 1
                if (pos-WIDTH+1) >= 0 and (pos-WIDTH+1) // WIDTH == row - 1 and board[pos-WIDTH+1] == OPTIONS[1-turn]:
                    while (pos-counter*WIDTH + counter) >= 0 and (pos-WIDTH*counter+counter) // WIDTH == row - counter and board[pos-counter*WIDTH+counter] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos-counter*WIDTH+counter) >= 0 and (pos-WIDTH*counter+counter) // WIDTH == row - counter and board[pos-counter*WIDTH+counter] == ".":
                        moves.add(pos-counter*WIDTH + counter)
                    counter = 1
                if (pos-WIDTH-1) >= 0 and (pos-WIDTH-1) // WIDTH == (row - 1) and board[pos-WIDTH-1] == OPTIONS[1-turn]:
                    while (pos-counter*WIDTH - counter) >= 0 and (pos-WIDTH*counter-counter) // WIDTH == row - counter and board[pos-counter*WIDTH-counter] == OPTIONS[1-turn]:
                        counter += 1
                    if (pos-counter*WIDTH-counter) >= 0 and (pos-WIDTH*counter-counter) // WIDTH == row - counter and board[pos-counter*WIDTH-counter] == ".":
                        moves.add(pos-counter*WIDTH - counter)
                    counter = 1
    return moves


def boardformat(board):
    for i in range(HEIGHT):
        print(board[i*HEIGHT:i*HEIGHT+HEIGHT])
if sys.argv[1:]:
    setLookups(sys.argv[1:])
else:
    setLookups(["oooooooooooooooooxoooox.oxoxooxxooxxooxxooxoxooxoxxxoxoox.xooooo"])
#boardformat("".join(BOARD))
if ACTIVE:
    choices = posmoves(BOARD)
    if choices:
        print(choices)
    else:
        print("No Moves Possible")

