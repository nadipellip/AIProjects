import sys
global HEIGHT, WIDTH, SIZE, BOARD,TURN,MOVES,POSDCT,ACTIVE,ACT
OPTIONS = ("X", "O")
def setLookups(inputval):
    global HEIGHT, WIDTH, SIZE, BOARD,TURN,MOVES,POSDCT,ACTIVE,ACT
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
        elif val == "X" or val == "x":
            ACT = False
            TURN = 0
        elif val == "O" or val == "o":
            ACT = False
            TURN = 1
        elif "-" not in val:
            MOVES.append(val.upper())
    POSDCT = {str(i):i for i in range(SIZE)}
    alpha = "ABCDEFGH"
    for i in range(len(alpha)):
        for j in range(WIDTH):
            POSDCT[alpha[i]+str(j+1)] = j*WIDTH+i
def playmove(pos):
    global HEIGHT, WIDTH, SIZE, BOARD, TURN, MOVES, ACTIVE, ACT
    switch = {pos}
    counter = 1
    if (pos+1) // WIDTH == pos // WIDTH and BOARD[pos+1] == OPTIONS[1-TURN]:
        s = set()
        while (pos + counter) // WIDTH == pos//WIDTH and BOARD[pos+counter] == OPTIONS[1-TURN]:
            s.add(pos+counter)
            counter += 1
        if (pos + counter) // WIDTH == pos//WIDTH and BOARD[pos + counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos-1) // WIDTH == pos // WIDTH and BOARD[pos-1] == OPTIONS[1-TURN]:
        s = set()
        while (pos - counter) // WIDTH == pos//WIDTH and BOARD[pos-counter] == OPTIONS[1-TURN]:
            s.add(pos-counter)
            counter += 1
        if (pos - counter) // WIDTH == pos//WIDTH and BOARD[pos - counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos + WIDTH) < SIZE and BOARD[pos+WIDTH] == OPTIONS[1-TURN]:
        s = set()
        while (pos + counter*WIDTH) < SIZE and BOARD[pos+counter*WIDTH] == OPTIONS[1-TURN]:
            s.add(pos+counter*WIDTH)
            counter += 1
        if (pos + counter*WIDTH) < SIZE and BOARD[pos + counter*WIDTH] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos + WIDTH) >= 0 and BOARD[pos-WIDTH] == OPTIONS[1-TURN]:
        s = set()
        while (pos - counter*WIDTH) >= 0 and BOARD[pos - counter*WIDTH] == OPTIONS[1-TURN]:
            s.add(pos - counter*WIDTH)
            counter += 1
        if (pos - counter*WIDTH) >= 0 and BOARD[pos - counter*WIDTH] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1

    if (pos + WIDTH + 1) < SIZE and (pos + WIDTH + 1) // WIDTH == pos//WIDTH + 1 and BOARD[pos + WIDTH + 1] == OPTIONS[
        1 - TURN]:
        s = set()
        while (pos + counter * WIDTH + counter) < SIZE and (
                pos + WIDTH * counter + counter) // WIDTH == pos//WIDTH + counter and BOARD[pos + counter * WIDTH + counter] == \
                OPTIONS[1 - TURN]:
            s.add(pos + counter*WIDTH+counter)
            counter += 1
        if (pos + counter * WIDTH + counter) < SIZE and (pos + WIDTH * counter + counter) // WIDTH == pos//WIDTH + counter and \
                BOARD[pos + counter * WIDTH + counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos + WIDTH - 1) < SIZE and (pos + WIDTH - 1) // WIDTH == pos//WIDTH + 1 and BOARD[pos + WIDTH - 1] == OPTIONS[
        1 - TURN]:
        s = set()
        while (pos + counter * WIDTH - counter) < SIZE and (
                pos + WIDTH * counter - counter) // WIDTH == pos//WIDTH + counter and BOARD[pos + counter * WIDTH - counter] == \
                OPTIONS[1 - TURN]:
            s.add(pos + counter * WIDTH - counter)
            counter += 1
        if (pos + counter * WIDTH - counter) < SIZE and (pos + WIDTH * counter - counter) // WIDTH == pos//WIDTH + counter and \
                BOARD[pos + counter * WIDTH - counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos - WIDTH + 1) >= 0 and (pos - WIDTH + 1) // WIDTH == pos // WIDTH - 1 and BOARD[pos - WIDTH + 1] == OPTIONS[1 - TURN]:
        s = set()
        while (pos - counter * WIDTH + counter) >= 0 and (pos - WIDTH * counter + counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH + counter] == OPTIONS[1 - TURN]:
            s.add(pos - counter * WIDTH + counter)
            counter += 1
        if (pos - counter * WIDTH + counter) >= 0 and (pos - WIDTH * counter + counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH + counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos - WIDTH - 1) >= 0 and (pos - WIDTH - 1) // WIDTH == (pos//WIDTH - 1) and BOARD[pos - WIDTH - 1] == OPTIONS[
        1 - TURN]:
        s = set()
        while (pos - counter * WIDTH - counter) >= 0 and (pos - WIDTH * counter - counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH - counter] == OPTIONS[1-TURN]:
            s.add(pos - counter * WIDTH - counter)
            counter += 1
        if (pos - counter * WIDTH - counter) >= 0 and (pos - WIDTH * counter - counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH - counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    b = [*BOARD]
    for i in switch:
        b[i] = OPTIONS[TURN]
    BOARD = "".join(b)
    TURN = 1 - TURN

def posmoves():
    global HEIGHT, WIDTH, SIZE, BOARD,TURN,MOVES, ACTIVE,ACT
    if ACT:
        TURN = BOARD.count(".")%2
        letter = OPTIONS[TURN]
        ACT = False
    else:
        letter = OPTIONS[TURN]
    moves = set()
    counter = 1
    for row in range(HEIGHT):
        for col in range(WIDTH):
            pos = row*WIDTH+col
            if BOARD[pos] == letter:
                if (pos+1)//WIDTH == row and BOARD[pos+1] == OPTIONS[1-TURN]:
                    while (pos+counter) // WIDTH == row and BOARD[pos+counter] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos+counter) // WIDTH == row and BOARD[pos+counter] == ".":
                        moves.add(pos+counter)
                    counter = 1
                if (pos-1)//WIDTH == row and BOARD[pos-1] == OPTIONS[1-TURN]:
                    while (pos-counter) // WIDTH == row and BOARD[pos-counter] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos-counter) // WIDTH == row and BOARD[pos-counter] == ".":
                        moves.add(pos-counter)
                    counter = 1
                if (pos+WIDTH) < SIZE and BOARD[pos+WIDTH] == OPTIONS[1-TURN]:
                    while (pos+counter*WIDTH) < SIZE and BOARD[pos+counter*WIDTH] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos+counter*WIDTH) < SIZE and BOARD[pos+counter*WIDTH] == ".":
                        moves.add(pos+counter*WIDTH)
                    counter = 1
                if (pos-WIDTH) >= 0 and BOARD[pos-WIDTH] == OPTIONS[1-TURN]:
                    while (pos-counter*WIDTH) >= 0 and BOARD[pos-counter*WIDTH] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos-counter*WIDTH) >= 0 and BOARD[pos-counter*WIDTH] == ".":
                        moves.add(pos-counter*WIDTH)
                    counter = 1
                if (pos+WIDTH+1) < SIZE and (pos+WIDTH+1) // WIDTH == row + 1 and BOARD[pos+WIDTH+1] == OPTIONS[1-TURN]:
                    while (pos+counter*WIDTH + counter) < SIZE and (pos+WIDTH*counter+counter) // WIDTH == row+counter and BOARD[pos+counter*WIDTH+counter] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos+counter*WIDTH+counter) < SIZE and (pos+WIDTH*counter+counter) // WIDTH == row + counter and BOARD[pos+counter*WIDTH+counter] == ".":
                        moves.add(pos+counter*WIDTH + counter)
                    counter = 1
                if (pos+WIDTH-1) < SIZE and (pos+WIDTH-1) // WIDTH == row + 1 and BOARD[pos+WIDTH-1] == OPTIONS[1-TURN]:
                    while (pos+counter*WIDTH - counter) < SIZE and (pos+WIDTH*counter-counter) // WIDTH == row + counter and BOARD[pos+counter*WIDTH-counter] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos+counter*WIDTH-counter) < SIZE and (pos+WIDTH*counter-counter) // WIDTH == row + counter and BOARD[pos+counter*WIDTH-counter] == ".":
                        moves.add(pos+counter*WIDTH - counter)
                    counter = 1
                if (pos-WIDTH+1) >= 0 and (pos-WIDTH+1) // WIDTH == row - 1 and BOARD[pos-WIDTH+1] == OPTIONS[1-TURN]:
                    while (pos-counter*WIDTH + counter) >= 0 and (pos-WIDTH*counter+counter) // WIDTH == row - counter and BOARD[pos-counter*WIDTH+counter] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos-counter*WIDTH+counter) >= 0 and (pos-WIDTH*counter+counter) // WIDTH == row - counter and BOARD[pos-counter*WIDTH+counter] == ".":
                        moves.add(pos-counter*WIDTH + counter)
                    counter = 1
                if (pos-WIDTH-1) >= 0 and (pos-WIDTH-1) // WIDTH == (row - 1) and BOARD[pos-WIDTH-1] == OPTIONS[1-TURN]:
                    while (pos-counter*WIDTH - counter) >= 0 and (pos-WIDTH*counter-counter) // WIDTH == row - counter and BOARD[pos-counter*WIDTH-counter] == OPTIONS[1-TURN]:
                        counter += 1
                    if (pos-counter*WIDTH-counter) >= 0 and (pos-WIDTH*counter-counter) // WIDTH == row - counter and BOARD[pos-counter*WIDTH-counter] == ".":
                        moves.add(pos-counter*WIDTH - counter)
                    counter = 1
    return moves


def boardformat(BOARD):
    for i in range(HEIGHT):
        print(BOARD[i*HEIGHT:i*HEIGHT+HEIGHT])
if sys.argv[:]:
    setLookups(sys.argv[1:])
else:
    setLookups([])
boardformat(BOARD)
print("Board: " + BOARD)
print(str(BOARD.count("X")) + "/" + str(BOARD.count("O")))
p = posmoves()
if not p:
    TURN = 1 - TURN
print("Possible moves for " + OPTIONS[TURN] + ": " + str(p))
if ACTIVE:
    for move in MOVES:
        if POSDCT[move] in posmoves():
            print(OPTIONS[TURN] + " plays to " + str(POSDCT[move]))
            playmove(POSDCT[move])
            boardformat(BOARD)
            print("Board: " + BOARD)
            print(str(BOARD.count("X")) + "/" + str(BOARD.count("O")))
            p = posmoves()
            if p:
                print("Possible moves for " + OPTIONS[TURN] + ": " + str(p))
            else:
                print(OPTIONS[TURN] + " passes their turn")
                TURN = 1 - TURN
                l = posmoves()
                print("Possible moves for " + OPTIONS[TURN] + ": " + str(l))
            print()