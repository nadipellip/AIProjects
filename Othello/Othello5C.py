"""
def negamax(brd,token):
    returns a list of best minScore followed by optimal move sequence in reverse
    if brd is terminal(no possible moves for either player or full):
        return [score]
    if no moves for token:
        do what necessary
    nmList = [negamax(makeMove(brd,token,mv), enemy) + [mv] for mv in moves]
    best = sorted(nmList)(appropriate Index)
    return best modified appropriately

Improvements
def negamax(brd,token) or (brd,token level):
    returns a list of best minScore followed by optimal move sequence in reverse
    if brd is terminal(no possible moves for either player or full):
        return [score]
    if no moves for token:
        do what necessary
    #nmList = [negamax(makeMove(brd,token,mv), enemy, level+1) + [mv] for mv in moves
    best = [-len(brd) - 1]
    for mv in moves:
        nM = negamax(makeMove(brd,tkn),enemy) + [mv]
        if nM is better:
            print the new nm(only at the top level)
            best = nm
    best = sorted(nmList)(appropriate Index)
    return best modified appropriately
1. Caching
    a. returned negamax values
2. How Terminal boards are determined
    a. If you know what tokens will be flipped upon a move, then if there is exactly one hole left, the resultant score can be computed exactly
3. Use explicit for loop to print out everytime you make an improvement(VERY IMPORTANT!!!!!!!!!!!)
"""
import sys

global HEIGHT, WIDTH, SIZE, BOARD, TURN, MOVES, POSDCT,MINICACHE,POSMOVESCACHE
OPTIONS = ("X", "O")
CORNERS = {0, 7, 56, 63}
BADSPOTS = {1: 0, 6: 7, 8: 0, 9: 0, 14: 7, 15: 7, 48: 56, 49: 56, 54: 63, 55: 63, 57: 56, 62: 63}
DIRECTIONS = [-1,-9,-8,-7,1,9,8,7]
def minimax(brd, tkn,depth):
    if (brd,tkn) in POSMOVESCACHE:
        moves = POSMOVESCACHE[(brd,tkn)]
    else:
        moves = posmoves(brd, tkn)
        POSMOVESCACHE[(brd,tkn)] = moves
    if (brd,tkn) in MINICACHE:
        return MINICACHE[(brd,tkn)]
    else:
        if not moves:
            if (brd, 1 - tkn) in POSMOVESCACHE:
                enemy = POSMOVESCACHE[(brd, 1 - tkn)]
            else:
                enemy = posmoves(brd, 1 - tkn)
                POSMOVESCACHE[(brd, 1 - tkn)] = enemy
            if not (moves or enemy):
                return [brd.count(OPTIONS[TURN]) - brd.count(OPTIONS[1 - TURN])]
            else:
                bestValue = minimax(brd,1-tkn,depth+1)+[-1]
                MINICACHE[(brd,tkn)] = bestValue
                return bestValue
        else:
            if tkn == TURN:
                bestValue = [-len(brd) - 1]
                for mv in moves:
                    totctr,newbrd = playmove(brd,tkn,mv)
                    mm = minimax(newbrd,1-tkn,depth+1) + [mv]
                    if mm[0] > bestValue[0]:
                        MINICACHE[(brd, tkn)] = mm
                        bestValue = mm
                        if depth == 0:
                            print("Min score: " + str(bestValue[0])+"; move sequence: " + str(bestValue[1:]))
                return bestValue
            else: # minimizingPlayer
                bestValue = [len(brd)+1]
                for mv in moves:
                    totctr,newbrd = playmove(brd,tkn,mv)
                    mm = minimax(newbrd,1-tkn,depth+1) + [mv]
                    if mm[0] < bestValue[0]:
                        MINICACHE[(brd, tkn)] = mm
                        bestValue = mm
                        if depth == 0:
                            print("Min score: " + str(bestValue[0])+"; move sequence: " + str(bestValue[1:]))
                return bestValue

def setLookups(inputval):
    global HEIGHT, WIDTH, SIZE, BOARD, TURN, MOVES, POSDCT, CORNERCONNECTS, MINICACHE,POSMOVESCACHE, INTDIVIDE,ABS,FOURMOD,TWOMOD
    act = True
    MINICACHE = {}
    POSMOVESCACHE = {}
    HEIGHT = 8
    WIDTH = 8
    SIZE = HEIGHT * WIDTH
    BOARD = ["." for i in range(SIZE)]
    BOARD[27], BOARD[28] = "O", "X"
    BOARD[35], BOARD[36] = "X", "O"
    BOARD = "".join(BOARD)
    BOARD = BOARD.upper()
    MOVES = []
    for val in inputval:
        if len(val) == 64:
            BOARD = val.upper()
        elif val == "X" or val == "x":
            TURN = 0
            act = False
        elif val == "O" or val == "o":
            TURN = 1
            act = False
        elif "-" not in val:
            MOVES.append(val.upper())
    if act:
        TURN = BOARD.count(".") % 2
    POSDCT = {str(i): i for i in range(SIZE)}
    alpha = "ABCDEFGH"
    for i in range(len(alpha)):
        for j in range(WIDTH):
            POSDCT[alpha[i] + str(j + 1)] = j * WIDTH + i
    CORNERCONNECTS = {i for i in range(SIZE) if i % WIDTH == 0 or i % WIDTH == 7 or i // WIDTH == 0 or i // WIDTH == 7}
    INTDIVIDE = {i:i//WIDTH for i in range(SIZE)}
    ABS = {i-64:abs(i-64) for i in range(SIZE*2)}
    FOURMOD = {i:(i%4==0) for i in range(WIDTH)}
    TWOMOD = {i: (i % 2 == 1) for i in range(WIDTH)}

def playmove(brd, tkn,mv): # assuming valid move
    # total number of opponent pieces taken
    brd = [*brd]
    brd[mv] = OPTIONS[tkn]
    totctr = 0
    for d in range(8): # 8 directions
        ctr = 0
        for n in range(8):
            pos = mv + DIRECTIONS[d] * (n + 1)
            if pos < 0 or pos >= SIZE or (FOURMOD[d] and (INTDIVIDE[pos] != INTDIVIDE[mv])) or (TWOMOD[d] and ABS[INTDIVIDE[pos] - INTDIVIDE[mv]] != (n + 1)):
                ctr = 0
                break
            elif brd[pos] == OPTIONS[tkn]:
                totctr += ctr
                break
            elif brd[pos] == ".":
                ctr = 0
                break
            else:
                ctr += 1
        for i in range(ctr):
            brd[mv+DIRECTIONS[d]*(i+1)] = OPTIONS[tkn]
    return (totctr,"".join(brd))


def posmoves(brd, tkn):
    moves = set()
    for i in range(SIZE):
        if brd[i] == OPTIONS[tkn]:
            for d in range(8):  # 8 directions
                for n in range(WIDTH):
                    pos = i + DIRECTIONS[d] * (n + 1)
                    if pos < 0 or pos >= SIZE or (FOURMOD[d] and (INTDIVIDE[pos]) != (INTDIVIDE[i])) or (TWOMOD[d] and ABS[INTDIVIDE[pos] - INTDIVIDE[i]] != (n + 1)):
                        break
                    elif brd[pos] == "." and n:
                        moves.add(pos)
                        break
                    elif brd[pos] != OPTIONS[1-tkn]:
                        break
    return moves



def choosePos(brd, tkn, choices):
    corners = set()
    good = set()
    neutral = set()
    bad = set()
    for pos in choices:
        if pos in CORNERS:
            corners.add(pos)
        elif pos in BADSPOTS:
            if brd[BADSPOTS[pos]] == OPTIONS[tkn]:
                good.add(pos)
            else:
                bad.add(pos)
        elif pos in CORNERCONNECTS:
            if isconnected(brd, tkn, pos):
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


def isconnected(brd, tkn, pos):
    if pos // WIDTH == 0 or pos // WIDTH == 7:
        # going right
        count = 1
        while pos + count < SIZE and (pos + count) in CORNERCONNECTS and brd[pos + count] == OPTIONS[1 - tkn]:
            count += 1
        if (pos + count) in CORNERS and brd[pos + count] == OPTIONS[tkn]:
            return True
        # going left
        count = 1
        while pos - count > 0 and (pos - count) in CORNERCONNECTS and brd[pos - count] == OPTIONS[1 - tkn]:
            count += 1
        if (pos - count) in CORNERS and brd[pos - count] == OPTIONS[tkn]:
            return True
    if pos % WIDTH == 0 or pos % WIDTH == 7:
        count = 1
        while pos + count * WIDTH < SIZE and (pos + count * WIDTH) in CORNERCONNECTS and brd[pos + count * WIDTH] == \
                OPTIONS[1 - tkn]:
            count += 1
        if (pos + count * WIDTH) in CORNERS and brd[pos + count * WIDTH] == OPTIONS[tkn]:
            return True
        count = 1
        while pos - count * WIDTH > 0 and (pos - count * WIDTH) in CORNERCONNECTS and brd[pos - count * WIDTH] == \
                OPTIONS[1 - tkn]:
            count += 1
        if (pos - count * WIDTH) in CORNERS and brd[pos - count * WIDTH] == OPTIONS[tkn]:
            return True

    return False


def boardformat(board):
    for i in range(HEIGHT):
        print(board[i * HEIGHT:i * HEIGHT + HEIGHT])
if sys.argv[1:]:
    setLookups(sys.argv[1:])
else:
    setLookups([])
boardformat(BOARD)
print("Board: " + BOARD)
print(str(BOARD.count("X")) + "/" + str(BOARD.count("O")))
p = posmoves(BOARD, TURN)
if not p:
    TURN = 1 - TURN
print("Possible moves for " + OPTIONS[TURN] + ": " + str(p))
for move in MOVES:
    if POSDCT[move] in posmoves(BOARD,TURN):
        print(OPTIONS[TURN] + " plays to " + str(POSDCT[move]))
        BOARD = playmove(BOARD,TURN,POSDCT[move])
        TURN = 1 - TURN
        boardformat(BOARD)
        print("Board: " + BOARD)
        print(str(BOARD.count("X")) + "/" + str(BOARD.count("O")))
        p = posmoves(BOARD,TURN)
        if p:
            print("Possible moves for " + OPTIONS[TURN] + ": " + str(p))
        else:
            print(OPTIONS[TURN] + " passes their turn")
            TURN = 1 - TURN
            l = posmoves(BOARD,TURN)
            print("Possible moves for " + OPTIONS[TURN] + ": " + str(l))
        print()
if not p:
    print("Game Over")
else:
    move = choosePos(BOARD, TURN, p)
    print(OPTIONS[TURN] + " plays to " + str(move))
    if (BOARD.count(".") < 11):
        nm = minimax(BOARD, TURN,0)
        print("Min score: " + str(nm[0])+"; move sequence: " + str(nm[1:]))
        #print(ABS)