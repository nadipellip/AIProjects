import sys
import re
from time import time

global PATTERNCACHE, SUCCESS
PATTERNCACHE = {}


def setGlobals(input):
    global NUMBLOCKS, HEIGHT, WIDTH, WORDDICT, SEEDSTRINGS, SIZE, CONNECTIONS, EXPLORED, EDGES, WORDSSET, INTDIVIDE, WORDHUER, WORDCONSTRAINTS
    WORDCONSTRAINTS = {}
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
    INTDIVIDE = {i: i // WIDTH for i in range(SIZE + WIDTH)}


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
    return (right * left + up * down) * -1


def readDict(f):
    global WORDSSET, WORDHUER
    WORDHUER = {}
    words = open(f, 'r').read().splitlines()
    WORDSSET = set(words)
    words = scorefile(words)
    wdict = {}
    for word in words:
        length = len(word[1])
        WORDHUER[word[1]] = word[0]
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
    alphascore = {a: alphascore[a] for a in alphascore}
    words = []
    for word in l:
        score = 0
        for i in range(len(word)):
            score += alphascore[word[i]]
        words.append((score * -1, word))
    return words


def timeformat(t):
    ti = ("{0:.3g}".format(t))
    if "e" in ti:
        return "0." + "0" * int(ti[ti.find("e") + 2:]) + ti[:ti.find("e")].replace(".", "")
    return ti + "s"


# Crossword2
def geninitconstraints(board):
    hvisited = set()
    vvisited = set()
    for i in range(SIZE):
        if board[i] != "#":
            if i not in hvisited:
                count = 0
                temp = []
                while INTDIVIDE[i + count] == INTDIVIDE[i] and board[i + count] != "#":
                    hvisited.add(i + count)
                    temp.append(i + count)
                    count += 1
                WORDCONSTRAINTS[(i, "h")] = temp
            if i not in vvisited:
                count = 0
                temp = []
                while (i + count * WIDTH) < SIZE and board[i + count * WIDTH] != "#":
                    vvisited.add(i + count * WIDTH)
                    temp.append(i + count * WIDTH)
                    count += 1
                WORDCONSTRAINTS[(i, "v")] = temp


def findposword(pos, orientation, board):
    constraint = WORDCONSTRAINTS[pos, orientation]
    wordlen = len(constraint)
    count = 0
    scount = 0
    poswords = []
    for c in constraint:
        if board[c] != "-":
            pattern = count * "-" + board[c] + "-" * (wordlen - count - 1)
            if pattern in PATTERNCACHE:
                if scount == count:
                    poswords = PATTERNCACHE[pattern]
                elif poswords:
                    poswords = lintersection(poswords, PATTERNCACHE[pattern])
            else:
                words = []
                for word in WORDDICT[wordlen]:
                    if word[1][count] == board[c]:
                        words.append(word)
                PATTERNCACHE[pattern] = words
                if scount == count:
                    poswords = words
                elif poswords:
                    poswords = lintersection(poswords, words)
        else:
            scount += 1
        count += 1
    if scount == wordlen:
        return WORDDICT[wordlen],False
    return poswords,scount == 0


def isUnsolvable(board):
    used = []
    for pos in WORDCONSTRAINTS:
        posmoves,full = findposword(pos[0],pos[1],board)
        if not posmoves:
            return True
        if full:
            used.append(posmoves[0][1])
    return not(len(used) == len(set(used)))


def mostConstrained(board):
    poswords = set()
    for c in WORDCONSTRAINTS:
        tempwords,full = findposword(c[0],c[1],board)
        if not full:
           if tempwords:
               if not poswords:
                    poswords = tempwords
                    min = c
               elif len(tempwords) < len(poswords):
                    poswords = tempwords
                    min = c
    return min,poswords

def placeWord(board, pos, orientation, word):
    board = [*board]
    if orientation == "h":
        for i in range(len(word)):
            board[pos + i] = word[i]
    if orientation == "v":
        for i in range(len(word)):
            board[pos + i * WIDTH] = word[i]
    return "".join(board)


def solve(board):
    global SUCCESS
    if board.count("-") < SUCCESS:
        print(board)
        SUCCESS = board.count("-")
    if board.count("-") < SUCCESS:
        SUCCESS = board.count("-")
    if isUnsolvable(board):
        return
    if board.count("-") == 0:
        return board
    pos, poswords = mostConstrained(board)
    for word in poswords:
        newbrd = placeWord(board, pos[0], pos[1], word[1])
        newbrd = solve(newbrd)
        if newbrd:
            return newbrd


def lintersection(lst1, lst2):
    # Use of hybrid method
    lenone = len(lst1)
    lentwo = len(lst2)
    if lenone > + lentwo:
        temp = set(lst1)
        lst3 = [value for value in lst2 if value in temp]
        return lst3
    else:
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3


if sys.argv[1:]:
    start = time()
    setGlobals(sys.argv[1:])
    #setGlobals(["5x4", "0", "dct20k.txt"])
    board = placeSeedStrings(SEEDSTRINGS)
    print("Original Puzzle")
    boardformat(board)
    print("New Puzzle")
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
    geninitconstraints(board)
    print(isUnsolvable(board))
    #print(isUnsolvable("aaaasicam"))
    #print(findposword(0, "v", board))
    #print(PATTERNCACHE)
    #print(findposword(0,"v",board))
    SUCCESS = board.count("-")
    print(solve(board))
    print("Time: " + timeformat(time() - start))