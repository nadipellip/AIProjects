import sys
import re
from time import time


def setGlobals(input):
    global NUMBLOCKS, HEIGHT, WIDTH, WORDDICT, SEEDSTRINGS, SIZE, CONNECTIONS, EXPLORED, EDGES, WORDSSET
    WORDSSET = set()
    EXPLORED = set()
    EDGES = set()
    CONNECTIONS = set()
    SEEDSTRINGS = []
    for idx, item in enumerate(input):
        # item = item.lower()
        if idx == 0:
            HEIGHT = int(item[:item.find("x")])
            WIDTH = int(item[item.find("x") + 1:])
            SIZE = WIDTH * HEIGHT
        elif idx == 1:
            NUMBLOCKS = int(item)
        elif re.search(r"^.*txt$", item, re.I):
            WORDDICT = readDict(item)
        elif re.search(r"^(h|v).*$", item, re.I):
            item = item.lower()
            orientation = item[0]
            hd = item[1:item.find("x")]
            temp = item[item.find("x") + 1:]
            vd = ""
            i = 0
            while re.search(r"\d", temp[i]):
                vd += temp[i]
                i += 1
            word = temp[i:]
            SEEDSTRINGS.append((orientation, int(hd), int(vd), word))


def floodfill(board, pos):
    global CONNECTIONS
    # print(CONNECTIONS)
    if len(CONNECTIONS) == SIZE - board.count("#"):
        return True
    if pos in CONNECTIONS:
        return False
    if pos < 0 or pos >= SIZE:
        return False
    if board[pos] == "#":
        return False
    elif board[pos] != "#":
        CONNECTIONS.add(pos)
        if pos % WIDTH == 0:
            return floodfill(board, pos + 1) or floodfill(board, pos + WIDTH) or floodfill(board, pos - WIDTH)
        if pos % WIDTH == (WIDTH - 1):
            return floodfill(board, pos - 1) or floodfill(board, pos + WIDTH) or floodfill(board, pos - WIDTH)
        return floodfill(board, pos - 1) or floodfill(board, pos + 1) or floodfill(board, pos + WIDTH) or floodfill(
            board, pos - WIDTH)


def isConnected(board):
    global CONNECTIONS
    CONNECTIONS = set()
    pos = 0
    if board.count("#") == SIZE:
        return True
    while board[pos] == "#" and pos < SIZE:
        pos += 1
    if floodfill(board, pos):
        return True
    return False


def placeSeedStrings(s):
    board = ["-" for i in range(WIDTH * HEIGHT)]
    if s:
        for item in s:
            orientation = item[0]
            pos = item[1] * WIDTH + item[2]
            word = item[3]
            if orientation == "h":
                for i in range(len(word)):
                    board[pos + i] = word[i]
            if orientation == "v":
                for i in range(len(word)):
                    board[pos + i * WIDTH] = word[i]
    return "".join(board)


def boardformat(board):
    for i in range(HEIGHT):
        print(board[i * WIDTH:(i + 1) * WIDTH])


def bruteForce(board):
    newbrd = placeImpliedSquares(board)
    if not newbrd or isInvalid(newbrd):
        return
    if newbrd.count("#") == NUMBLOCKS:
        return newbrd
    board = [*newbrd]
    choices = choosePos(board)
    for pos in choices:
        board[pos[1]] = "#"
        newbrd = "".join(board)
        board[pos[1]] = "-"
        bF = bruteForce(newbrd)
        if bF:
            return bF


def isInvalid(board):
    return threelength(board) or not isConnected(board) or not isPalindrome(board)


def isPalindrome(board):
    board = [*board]
    for i in range(SIZE):
        if board[i] == "#":
            if board[SIZE - (i + 1)] != "#":
                return False
    return True


def threelength(board):
    validhorizontal = set()
    validvertical = set()
    for i in range(SIZE):
        if board[i] != "#":
            if i not in validhorizontal:
                s = {i}
                count = 1
                while ((i + count) // WIDTH) == (i // WIDTH) and board[i + count] != "#":
                    s.add(i + count)
                    count += 1
                if count >= 3:
                    validhorizontal = validhorizontal.union(s)
                else:
                    return True
            if i not in validvertical:
                s = {i}
                count = 1
                while (i + count * WIDTH) < SIZE and board[i + count * WIDTH] != "#":
                    s.add(i + count * WIDTH)
                    count += 1
                if count >= 3:
                    validvertical = validvertical.union(s)
                else:
                    return True
    return False


def placeImpliedThreeLength(board):
    validhorizontal = set()
    validvertical = set()
    for i in range(SIZE):
        if board[i] != "#":
            if i not in validhorizontal:
                s = {i}
                count = 1
                while ((i + count) // WIDTH) == (i // WIDTH) and board[i + count] != "#":
                    s.add(i + count)
                    count += 1
                if count >= 3:
                    validhorizontal = validhorizontal.union(s)
            if i not in validvertical:
                s = {i}
                count = 1
                while (i + count * WIDTH) < SIZE and board[i + count * WIDTH] != "#":
                    s.add(i + count * WIDTH)
                    count += 1
                if count >= 3:
                    validvertical = validvertical.union(s)
    posblocks = {i for i in range(SIZE) if board[i] == "-"}
    blocks = posblocks.difference(validvertical.intersection(validhorizontal))
    board = [*board]
    for b in blocks:
        board[b] = "#"
    return "".join(board)


def placeImpliedReflect(board):
    board = [*board]
    for i in range(SIZE):
        if board[i] == "#":
            if board[SIZE - (i + 1)] == "-":
                board[SIZE - (i + 1)] = "#"
            elif board[SIZE - (i + 1)] != "#":
                return
    return "".join(board)


def placeImpliedSquares(board):
    prevbrd = ""
    newbrd = board
    count = 0
    while threelength(newbrd) and prevbrd != newbrd or count == 0:
        prevbrd = newbrd
        newbrd = placeImpliedThreeLength(prevbrd)
        newbrd = placeImpliedFill(newbrd)
        newbrd = placeImpliedReflect(newbrd)
        if newbrd:
            newbrd = "".join(newbrd)
        else:
            return
        count += 1
    board = "".join(newbrd)
    # board = placeImpliedFill(board)
    if board.count("#") <= NUMBLOCKS:
        return board
    return


def containsReflect(l):
    for i in l:
        if SIZE - i in l:
            return True
        return False


def placeImpliedFill(board):
    global EDGES
    if not isConnected(board):
        for i in range(SIZE):
            if not i in EXPLORED:
                if board[i] != "#":
                    areafill(board, i)
                    if not containsReflect(EDGES):
                        newbrd = [*board]
                        for e in EDGES:
                            newbrd[e] = "#"
                        newbrd = "".join(newbrd)
                        if isConnected(newbrd):
                            board = newbrd
                    EDGES = set()

                else:
                    EXPLORED.add(i)
    return board


def areafill(board, pos):
    if len(CONNECTIONS) == SIZE - board.count("#"):
        return True
    if pos in CONNECTIONS:
        return False
    if pos < 0 or pos >= SIZE:
        return False
    if board[pos] == "#":
        EXPLORED.add(pos)
        return False
    elif board[pos] != "#":
        EDGES.add(pos)
        EXPLORED.add(pos)
        if pos % WIDTH == 0:
            return floodfill(board, pos + 1) or floodfill(board, pos + WIDTH) or floodfill(board, pos - WIDTH)
        if pos % WIDTH == (WIDTH - 1):
            return floodfill(board, pos - 1) or floodfill(board, pos + WIDTH) or floodfill(board, pos - WIDTH)
        return floodfill(board, pos - 1) or floodfill(board, pos + 1) or floodfill(board, pos + WIDTH) or floodfill(
            board, pos - WIDTH)


def choosePos(board):
    choices = []
    for i in range(SIZE):
        if board[i] == "-":
            choices.append((posheur(board, i), i))
    return sorted(choices)


def posheur(board, pos):
    row = pos // WIDTH
    right = 0
    while (pos + right) // WIDTH == row and board[pos + right] != "#":
        right += 1
    left = 0
    while (pos - left) // WIDTH == row and board[pos - left] != "#":
        left += 1
    up = 0
    while (pos + up * WIDTH) < SIZE and board[pos + up * WIDTH] != "#":
        up += 1
    down = 0
    while (pos - down * WIDTH) > 0 and board[pos - down * WIDTH] != "#":
        down += 1
    return min(right, left) * min(up, down) * -1


def readDict(f):
    global WORDSSET
    words = open(f, 'r').read().splitlines()
    # WORDSSET = set(words)
    words = scorefile(words)
    wdict = {}
    for word in words:
        length = len(word[1])
        if length not in wdict:
            wdict[length] = [(word[0], word[1])]
        else:
            wdict[length].append((word[0], word[1]))
    for i in wdict:
        wdict[i].sort()
    return wdict


def scorefile(l):
    alphascore = {}
    for word in l:
        for i in range(len(word)):
            if word[i] not in alphascore:
                alphascore[word[i]] = 1
            else:
                alphascore[word[i]] += 1
    alphascore = {a: alphascore[a] // 100 for a in alphascore}
    words = []
    for word in l:
        score = 0
        for i in range(len(word)):
            score += alphascore[word[i]]
        words.append((score * -1, word))
    return words


def isUnsolvable(board, constraints):
    for c in constraints:
        if constraints[c] != 0:
            if not islegalword(board, c[1], c[0]):
                return True
    return False


def solve(board, constraints):
    used = usedwords(board, constraints)
    if len(set(used)) != len(used):
        # boardformat(board)
        # print(used)
        return
    if isUnsolvable(board, constraints):
        return
    if board.count("-") == 0:
        return board
    # print(constraints)
    npos = mostconstrained(constraints)
    # print(npos)
    words = legalword(board, npos[1], npos[0])
    # print()
    # boardformat(board)
    # nconst = updateConstraints(constraints, board, npos[0], npos[1])
    # print(nconst)
    nconst = 0
    for word in words:
        if word not in used:
            newbrd = placeword(board, npos[1], npos[0], word[1])
            # boardformat(newbrd)
            if nconst == 0:
                # nconst = updateConstraints(constraints,newbrd,npos[0],npos[1])
                # boardformat(newbrd)
                nconst = genConstraints(newbrd)
                # print(nconst)
            bF = solve(newbrd, nconst)
            if bF:
                return bF


def mostconstrained(constraints):
    min = 0
    for i in constraints:
        if min == 0:
            min = i
        if constraints[i] != 0 and constraints[i] < constraints[min] or constraints[min] == 0:
            min = i
    return min


def placeword(board, orientation, pos, word):
    board = [*board]
    if orientation == "h":
        for i in range(len(word)):
            board[pos + i] = word[i]
    if orientation == "v":
        for i in range(len(word)):
            board[pos + i * WIDTH] = word[i]
    return "".join(board)


def updateConstraints(constraints, board, pos, orientation):
    if orientation == "h":
        i = 0
        while (pos + i) // WIDTH == pos // WIDTH and board[pos + i] != "#":
            newpos = pos + i
            ucount = 0
            uscount = 0
            while newpos - WIDTH * ucount >= 0 and board[newpos - WIDTH * ucount] != "#":
                if board[newpos - WIDTH * ucount] == "-":
                    uscount += 1
                ucount += 1
            dcount = 1
            dscount = 0
            while newpos + WIDTH * dcount < SIZE and board[newpos + WIDTH * dcount] != "#":
                if board[newpos + WIDTH * dcount] == "-":
                    dscount += 1
                dcount += 1
            constraints[newpos - WIDTH * (ucount - 1), "v"] = uscount + dscount
            i += 1
    if orientation == "v":
        i = 0
        while pos + i * WIDTH < SIZE and board[pos + i * WIDTH] != "#":
            newpos = pos + i * WIDTH
            lcount = 0
            lscount = 0
            while (newpos - lcount) // WIDTH == newpos // WIDTH and board[newpos - lcount] != "#":
                if board[newpos - lcount] == "-":
                    lscount += 1
                lcount += 1
            rcount = 1
            rscount = 0
            while (newpos + rcount) // WIDTH == newpos // WIDTH and board[newpos + rcount] != "#":
                if board[newpos + rcount] == "-":
                    rscount += 1
                rcount += 1
            constraints[newpos - lcount + 1, "h"] = rscount + lscount
            i += 1
    constraints[pos, orientation] = 0
    return constraints


def genConstraints(board):
    constraints = {}
    hvisited = set()
    vvisited = set()
    for i in range(SIZE):
        if board[i] != "#":
            if i not in hvisited:
                lettercount = 0
                count = 0
                while (i + count) // WIDTH == i // WIDTH and board[i + count] != "#":
                    hvisited.add(i + count)
                    if board[i + count] != "-":
                        lettercount += 1
                    count += 1
                constraints[(i, "h")] = count - lettercount
            if i not in vvisited:
                lettercount = 0
                count = 0
                while (i + count * WIDTH) < SIZE and board[i + count * WIDTH] != "#":
                    vvisited.add(i + count * WIDTH)
                    if board[i + count * WIDTH] != "-":
                        lettercount += 1
                    count += 1
                constraints[(i, "v")] = count - lettercount
    return constraints


def usedwords(board, constraints):
    words = []
    for c in constraints:
        if constraints[c] == 0:
            if c[1] == "h":
                count = 0
                tempstr = ""
                while (c[0] + count) // WIDTH == c[0] // WIDTH and board[c[0] + count] != "#":
                    tempstr += board[c[0] + count]
                    count += 1
                words.append(tempstr)
            if c[1] == "v":
                count = 0
                tempstr = ""
                while (c[0] + count * WIDTH) < SIZE and board[c[0] + count * WIDTH] != "#":
                    tempstr += board[c[0] + count * WIDTH]
                    count += 1
                words.append(tempstr)
    return words


def legalword(board, orientation, pos):
    words = []
    if orientation == "h":
        constraints = []
        right = 0
        while (pos + right) // WIDTH == pos // WIDTH and board[pos + right] != "#":
            if board[pos + right] != "-":
                constraints.append((right, board[pos + right]))
            right += 1
        if len(constraints) == right:
            return
        # print(constraints)
        for word in WORDDICT[right]:
            if satisfy(constraints, word[1]):
                words.append(word)
        return words
    if orientation == "v":
        constraints = []
        down = 0
        while pos + down * WIDTH < SIZE and board[pos + down * WIDTH] != "#":
            if board[pos + down * WIDTH] != "-":
                constraints.append((down, board[pos + down * WIDTH]))
            down += 1
        if len(constraints) == down:
            return
        # print(constraints)
        for word in WORDDICT[down]:
            if satisfy(constraints, word[1]):
                words.append(word)
        return words
    return


def satisfy(constraint, word):
    for c in constraint:
        if word[c[0]] != c[1]:
            return False
    return True


def islegalword(board, orientation, pos):
    if orientation == "h":
        constraints = []
        right = 0
        tempstr = ""
        while (pos + right) // WIDTH == pos // WIDTH and board[pos + right] != "#":
            tempstr += board[pos + right]
            if board[pos + right] != "-":
                constraints.append((right, board[pos + right]))
            right += 1
        for word in WORDDICT[right]:
            if tempstr in WORDSSET or satisfy(constraints, word[1]):
                return True
        return False
    if orientation == "v":
        constraints = []
        down = 0
        tempstr = ""
        while pos + down * WIDTH < SIZE and board[pos + down * WIDTH] != "#":
            tempstr += board[pos + down * WIDTH]
            if board[pos + down * WIDTH] != "-":
                constraints.append((down, board[pos + down * WIDTH]))
            down += 1
        for word in WORDDICT[down]:
            if tempstr in WORDSSET or satisfy(constraints, word[1]):
                return True
        return False


def timeformat(t):
    ti = ("{0:.3g}".format(t))
    if "e" in ti:
        return "0." + "0" * int(ti[ti.find("e") + 2:]) + ti[:ti.find("e")].replace(".", "")
    return ti + "s"


if sys.argv[1:]:
    """setGlobals(sys.argv[1:])
    board = placeSeedStrings(SEEDSTRINGS)
    print("Original Board:")
    boardformat(board)
    print("Board with Implied Squares:")
    board = placeImpliedSquares(board)
    boardformat(board)
    print("FloodFill")
    print(isConnected(board))"""
    start = time()
    setGlobals(sys.argv[1:])
    # print(WORDDICT)
    board = placeSeedStrings(SEEDSTRINGS)
    print("Original Puzzle")
    boardformat(board)
    print("New Puzzle")
    # boardformat(placeImpliedSquares(board))
    # boardformat("#####################################------####------####------#####################################")
    if NUMBLOCKS == HEIGHT * WIDTH:
        boardformat("#" * HEIGHT * WIDTH)
    else:
        if NUMBLOCKS == 0:
            boardformat(board)
        if WIDTH % 2 == 1 and HEIGHT % 2 == 1 and NUMBLOCKS % 2 == 1:
            board = [board[i] for i in range(SIZE)]
            board[WIDTH * (HEIGHT // 2) + (WIDTH // 2)] = "#"
            board = "".join(board)
        if board.count("#") < NUMBLOCKS:
            newbrd = bruteForce(board)
            boardformat(newbrd)
            board = newbrd
    board = "idahoeatonentreearns"
    initconstraints = genConstraints(board)
    # print(initconstraints)
    # board = placeword(board,"h",2,"act")
    # print()
    # boardformat(board)
    # const = updateConstraints(initconstraints,board,2,"h")
    # print(const)
    # print(legalword(board,"v",0))
    # print(isUnsolvable("aaat--s--",initconstraints))
    # boardformat("ieeesy--le--es--")
    # print(mostconstrained(genConstraints("ieeesy--le--es--")))
    print()
    print(isUnsolvable("idahoeatonentreearns",initconstraints))
    #boardformat(solve(board, initconstraints))
    #print("Time: " + timeformat(time() - start))
    # print(isUnsolvable(board,0,"h"))
    # print(usedwords(board,initconstraints))
    # boardformat(placeword(newbrd,"h",0,"dog"))
