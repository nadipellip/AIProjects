import sys
import re


def setGlobals(input):
    global NUMBLOCKS, HEIGHT, WIDTH, WORDDICT, SEEDSTRINGS, SIZE, CONNECTIONS, EXPLORED, EDGES, USEDWORDS
    EXPLORED = set()
    EDGES = set()
    CONNECTIONS = set()
    USEDWORDS = set()
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
    while board[pos] == "#" and pos < SIZE - 1:
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
    rowh = right * left
    colh = up * down
    return max(rowh, colh) * -1


def readDict(f):
    words = open(f, 'r').read().splitlines()
    wdict = {}
    for word in words:
        length = len(word)
        if length not in wdict:
            wdict[length] = {word}
        else:
            wdict[length].add(word)
    return wdict


def solve(board):
    board = [*board]
    for i in range(len(board)):
        if board[i] != "#":
            word = legalword(board, "h", i)
            if word:
                board = placeword(board, "h", i, word)
    return "".join(board)


def placeword(board, orientation, pos, word):
    board = [*board]
    if orientation == "h":
        for i in range(len(word)):
            board[pos + i] = word[i]
    if orientation == "v":
        for i in range(len(word)):
            board[pos + i * WIDTH] = word[i]
    return "".join(board)


def legalword(board, orientation, pos):
    if orientation == "h":
        constraints = []
        right = 0
        while (pos + right) // WIDTH == pos // WIDTH and board[pos + right] != "#":
            if board[pos + right] != "-":
                constraints.append((right, board[pos + right]))
            right += 1
        if len(constraints) == right:
            return
        #print(constraints)
        for word in WORDDICT[right]:
            if word not in USEDWORDS and satisfy(constraints, word):
                USEDWORDS.add(word)
                return word
    if orientation == "v":
        constraints = []
        down = 0
        while pos+down*WIDTH < SIZE and board[pos + down*WIDTH] != "#":
            if board[pos + down*WIDTH] != "-":
                constraints.append((down, board[pos + down*WIDTH]))
            down += 1
        if len(constraints) == down:
            return
        #print(constraints)
        for word in WORDDICT[down]:
            if word not in USEDWORDS and satisfy(constraints, word):
                USEDWORDS.add(word)
                return word
    return


def satisfy(constraint, word):
    for c in constraint:
        if word[c[0]] != c[1]:
            return False
    return True


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
            # print(satisfy([(0,'d'),(2,'t')],"dota"))
            # boardformat(placeword(newbrd,"h",0,"dog"))
    print("Solved Board")
    wordone = legalword(board,"v",board.find("-"))
    board = placeword(board,"v",board.find("-"),wordone)
    #boardformat(board)
    board = solve(board)
    boardformat(board)
