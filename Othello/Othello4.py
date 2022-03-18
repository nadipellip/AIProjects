import sys

global HEIGHT, WIDTH, SIZE, BOARD, TURN, MOVES, POSDCT, ACTIVE, ACT
OPTIONS = ("X", "O")
CORNERS = {0, 7, 56, 63}
BADSPOTS = {1: 0, 6: 7, 8: 0, 9: 0, 14: 7, 15: 7, 48: 56, 49: 56, 54: 63, 55: 63, 57: 56, 62: 63}


def setLookups(inputval):
    global HEIGHT, WIDTH, SIZE, BOARD, TURN, MOVES, POSDCT, ACTIVE, ACT, CORNERCONNECTS
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
    POSDCT = {str(i): i for i in range(SIZE)}
    alpha = "ABCDEFGH"
    for i in range(len(alpha)):
        for j in range(WIDTH):
            POSDCT[alpha[i] + str(j + 1)] = j * WIDTH + i
    CORNERCONNECTS = set()
    for i in range(SIZE):
        if (i % WIDTH == 0 or i % WIDTH == 7 or i // WIDTH == 0 or i // WIDTH == 7) and i not in CORNERS:
            CORNERCONNECTS.add(i)


def playmove(pos):
    global HEIGHT, WIDTH, SIZE, BOARD, TURN, MOVES, ACTIVE, ACT
    switch = {pos}
    counter = 1
    if (pos + 1) // WIDTH == pos // WIDTH and BOARD[pos + 1] == OPTIONS[1 - TURN]:
        s = set()
        while (pos + counter) // WIDTH == pos // WIDTH and BOARD[pos + counter] == OPTIONS[1 - TURN]:
            s.add(pos + counter)
            counter += 1
        if (pos + counter) // WIDTH == pos // WIDTH and BOARD[pos + counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos - 1) // WIDTH == pos // WIDTH and BOARD[pos - 1] == OPTIONS[1 - TURN]:
        s = set()
        while (pos - counter) // WIDTH == pos // WIDTH and BOARD[pos - counter] == OPTIONS[1 - TURN]:
            s.add(pos - counter)
            counter += 1
        if (pos - counter) // WIDTH == pos // WIDTH and BOARD[pos - counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos + WIDTH) < SIZE and BOARD[pos + WIDTH] == OPTIONS[1 - TURN]:
        s = set()
        while (pos + counter * WIDTH) < SIZE and BOARD[pos + counter * WIDTH] == OPTIONS[1 - TURN]:
            s.add(pos + counter * WIDTH)
            counter += 1
        if (pos + counter * WIDTH) < SIZE and BOARD[pos + counter * WIDTH] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos + WIDTH) >= 0 and BOARD[pos - WIDTH] == OPTIONS[1 - TURN]:
        s = set()
        while (pos - counter * WIDTH) >= 0 and BOARD[pos - counter * WIDTH] == OPTIONS[1 - TURN]:
            s.add(pos - counter * WIDTH)
            counter += 1
        if (pos - counter * WIDTH) >= 0 and BOARD[pos - counter * WIDTH] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1

    if (pos + WIDTH + 1) < SIZE and (pos + WIDTH + 1) // WIDTH == pos // WIDTH + 1 and BOARD[pos + WIDTH + 1] == \
            OPTIONS[
                1 - TURN]:
        s = set()
        while (pos + counter * WIDTH + counter) < SIZE and (
                pos + WIDTH * counter + counter) // WIDTH == pos // WIDTH + counter and BOARD[
            pos + counter * WIDTH + counter] == \
                OPTIONS[1 - TURN]:
            s.add(pos + counter * WIDTH + counter)
            counter += 1
        if (pos + counter * WIDTH + counter) < SIZE and (
                pos + WIDTH * counter + counter) // WIDTH == pos // WIDTH + counter and \
                BOARD[pos + counter * WIDTH + counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos + WIDTH - 1) < SIZE and (pos + WIDTH - 1) // WIDTH == pos // WIDTH + 1 and BOARD[pos + WIDTH - 1] == \
            OPTIONS[
                1 - TURN]:
        s = set()
        while (pos + counter * WIDTH - counter) < SIZE and (
                pos + WIDTH * counter - counter) // WIDTH == pos // WIDTH + counter and BOARD[
            pos + counter * WIDTH - counter] == \
                OPTIONS[1 - TURN]:
            s.add(pos + counter * WIDTH - counter)
            counter += 1
        if (pos + counter * WIDTH - counter) < SIZE and (
                pos + WIDTH * counter - counter) // WIDTH == pos // WIDTH + counter and \
                BOARD[pos + counter * WIDTH - counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos - WIDTH + 1) >= 0 and (pos - WIDTH + 1) // WIDTH == pos // WIDTH - 1 and BOARD[pos - WIDTH + 1] == OPTIONS[
        1 - TURN]:
        s = set()
        while (pos - counter * WIDTH + counter) >= 0 and (
                pos - WIDTH * counter + counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH + counter] == OPTIONS[1 - TURN]:
            s.add(pos - counter * WIDTH + counter)
            counter += 1
        if (pos - counter * WIDTH + counter) >= 0 and (
                pos - WIDTH * counter + counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH + counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    if (pos - WIDTH - 1) >= 0 and (pos - WIDTH - 1) // WIDTH == (pos // WIDTH - 1) and BOARD[pos - WIDTH - 1] == \
            OPTIONS[
                1 - TURN]:
        s = set()
        while (pos - counter * WIDTH - counter) >= 0 and (
                pos - WIDTH * counter - counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH - counter] == OPTIONS[1 - TURN]:
            s.add(pos - counter * WIDTH - counter)
            counter += 1
        if (pos - counter * WIDTH - counter) >= 0 and (
                pos - WIDTH * counter - counter) // WIDTH == pos // WIDTH - counter and \
                BOARD[pos - counter * WIDTH - counter] == OPTIONS[TURN]:
            switch = switch.union(s)
        counter = 1
    b = [*BOARD]
    for i in switch:
        b[i] = OPTIONS[TURN]
    BOARD = "".join(b)
    TURN = 1 - TURN


def posmoves():
    global HEIGHT, WIDTH, SIZE, BOARD, TURN, MOVES, ACTIVE, ACT
    if ACT:
        TURN = BOARD.count(".") % 2
        letter = OPTIONS[TURN]
        ACT = False
    else:
        letter = OPTIONS[TURN]
    moves = set()
    counter = 1
    for row in range(HEIGHT):
        for col in range(WIDTH):
            pos = row * WIDTH + col
            if BOARD[pos] == letter:
                if (pos + 1) // WIDTH == row and BOARD[pos + 1] == OPTIONS[1 - TURN]:
                    while (pos + counter) // WIDTH == row and BOARD[pos + counter] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos + counter) // WIDTH == row and BOARD[pos + counter] == ".":
                        moves.add(pos + counter)
                    counter = 1
                if (pos - 1) // WIDTH == row and BOARD[pos - 1] == OPTIONS[1 - TURN]:
                    while (pos - counter) // WIDTH == row and BOARD[pos - counter] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos - counter) // WIDTH == row and BOARD[pos - counter] == ".":
                        moves.add(pos - counter)
                    counter = 1
                if (pos + WIDTH) < SIZE and BOARD[pos + WIDTH] == OPTIONS[1 - TURN]:
                    while (pos + counter * WIDTH) < SIZE and BOARD[pos + counter * WIDTH] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos + counter * WIDTH) < SIZE and BOARD[pos + counter * WIDTH] == ".":
                        moves.add(pos + counter * WIDTH)
                    counter = 1
                if (pos - WIDTH) >= 0 and BOARD[pos - WIDTH] == OPTIONS[1 - TURN]:
                    while (pos - counter * WIDTH) >= 0 and BOARD[pos - counter * WIDTH] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos - counter * WIDTH) >= 0 and BOARD[pos - counter * WIDTH] == ".":
                        moves.add(pos - counter * WIDTH)
                    counter = 1
                if (pos + WIDTH + 1) < SIZE and (pos + WIDTH + 1) // WIDTH == row + 1 and BOARD[pos + WIDTH + 1] == \
                        OPTIONS[1 - TURN]:
                    while (pos + counter * WIDTH + counter) < SIZE and (
                            pos + WIDTH * counter + counter) // WIDTH == row + counter and BOARD[
                        pos + counter * WIDTH + counter] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos + counter * WIDTH + counter) < SIZE and (
                            pos + WIDTH * counter + counter) // WIDTH == row + counter and BOARD[
                        pos + counter * WIDTH + counter] == ".":
                        moves.add(pos + counter * WIDTH + counter)
                    counter = 1
                if (pos + WIDTH - 1) < SIZE and (pos + WIDTH - 1) // WIDTH == row + 1 and BOARD[pos + WIDTH - 1] == \
                        OPTIONS[1 - TURN]:
                    while (pos + counter * WIDTH - counter) < SIZE and (
                            pos + WIDTH * counter - counter) // WIDTH == row + counter and BOARD[
                        pos + counter * WIDTH - counter] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos + counter * WIDTH - counter) < SIZE and (
                            pos + WIDTH * counter - counter) // WIDTH == row + counter and BOARD[
                        pos + counter * WIDTH - counter] == ".":
                        moves.add(pos + counter * WIDTH - counter)
                    counter = 1
                if (pos - WIDTH + 1) >= 0 and (pos - WIDTH + 1) // WIDTH == row - 1 and BOARD[pos - WIDTH + 1] == \
                        OPTIONS[1 - TURN]:
                    while (pos - counter * WIDTH + counter) >= 0 and (
                            pos - WIDTH * counter + counter) // WIDTH == row - counter and BOARD[
                        pos - counter * WIDTH + counter] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos - counter * WIDTH + counter) >= 0 and (
                            pos - WIDTH * counter + counter) // WIDTH == row - counter and BOARD[
                        pos - counter * WIDTH + counter] == ".":
                        moves.add(pos - counter * WIDTH + counter)
                    counter = 1
                if (pos - WIDTH - 1) >= 0 and (pos - WIDTH - 1) // WIDTH == (row - 1) and BOARD[pos - WIDTH - 1] == \
                        OPTIONS[1 - TURN]:
                    while (pos - counter * WIDTH - counter) >= 0 and (
                            pos - WIDTH * counter - counter) // WIDTH == row - counter and BOARD[
                        pos - counter * WIDTH - counter] == OPTIONS[1 - TURN]:
                        counter += 1
                    if (pos - counter * WIDTH - counter) >= 0 and (
                            pos - WIDTH * counter - counter) // WIDTH == row - counter and BOARD[
                        pos - counter * WIDTH - counter] == ".":
                        moves.add(pos - counter * WIDTH - counter)
                    counter = 1
    return moves


def boardformat(BOARD):
    for i in range(HEIGHT):
        print(BOARD[i * HEIGHT:i * HEIGHT + HEIGHT])


def choosePos(choices):
    corners = set()
    good = set()
    neutral = set()
    bad = set()
    for pos in choices:
        if pos in CORNERS:
            corners.add(pos)
        elif pos in BADSPOTS:
            if BOARD[BADSPOTS[pos]] == OPTIONS[TURN]:
                good.add(pos)
            else:
                bad.add(pos)
        elif pos in CORNERCONNECTS:
            if isconnected(pos):
                good.add(pos)
            else:
                neutral.add(pos)
        else:
            neutral.add(pos)
    if corners:
        return min(corners)
    if good:
        return min(good)
    if neutral:
        return min(neutral)
    if bad:
        return min(bad)
    return min(choices)


def isconnected(pos):
    if pos // WIDTH == 0 or pos // WIDTH == 7:
        # going right
        count = 1
        while pos + count < SIZE and (pos + count) in CORNERCONNECTS and BOARD[pos + count] == OPTIONS[1 - TURN]:
            count += 1
        if (pos + count) in CORNERS and BOARD[pos + count] == OPTIONS[TURN]:
            return True
        # going left
        count = 1
        while pos - count > 0 and (pos - count) in CORNERCONNECTS and BOARD[pos - count] == OPTIONS[1 - TURN]:
            count += 1
        if (pos - count) in CORNERS and BOARD[pos - count] == OPTIONS[TURN]:
            return True
    if pos % WIDTH == 0 or pos % WIDTH == 7:
        count = 1
        while pos + count * WIDTH < SIZE and (pos + count * WIDTH) in CORNERCONNECTS and BOARD[pos + count * WIDTH] == \
                OPTIONS[1 - TURN]:
            count += 1
        if (pos + count * WIDTH) in CORNERS and BOARD[pos + count * WIDTH] == OPTIONS[TURN]:
            return True
        count = 1
        while pos - count * WIDTH > 0 and (pos - count * WIDTH) in CORNERCONNECTS and BOARD[pos - count * WIDTH] == \
                OPTIONS[1 - TURN]:
            count += 1
        if (pos - count * WIDTH) in CORNERS and BOARD[pos - count * WIDTH] == OPTIONS[TURN]:
            return True

    return False


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
if p:
    move = choosePos(p)
    print(OPTIONS[TURN] + " plays to " + str(move))
