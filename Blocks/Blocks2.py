from time import time
import sys


def setLookups(r):
    global WIDTH, HEIGHT, TRAYAREA, NUMBEROFRECTS, BLOCKS, LABELS
    WIDTH = r[0][0]
    HEIGHT = r[0][1]
    TRAYAREA = WIDTH * HEIGHT
    bucket = [[] for I in range(WIDTH * HEIGHT +1)]
    BLOCKS = []
    LABELS = {}
    labels = "abcdefghijklmnopqrstuvwxyz"
    counter = 0
    for i in r[1:]:
        area = i[0] * i[1]
        bucket[area].append((i[0], i[1], labels[counter]))
        LABELS[labels[counter]] = area
        counter += 1
    for i in range(TRAYAREA+1):
        if bucket[i]:
            for j in bucket[i]:
                BLOCKS.append(j)
    BLOCKS = BLOCKS[::-1]
    NUMBEROFRECTS = len(r) - 1


def isImpossible(rects):
    trayArea = WIDTH * HEIGHT
    totalblockArea = sum([i[0] * i[1] for i in rects[1:]])
    if trayArea < totalblockArea:
        return True
    for b in rects[1:]:
        if (b[0] > WIDTH and b[0] > HEIGHT) or (b[1] > WIDTH and b[1] > HEIGHT):
            return True
    if trayArea == totalblockArea:
        wparity = WIDTH % 2
        hparity = HEIGHT % 2
        if wparity or hparity:
            for r in rects[1:]:
                if r[0] % 2 == 1 or r[1] % 2 == 1:
                    return False
            return True
    return False


def isSolved(tray):
    return len(set(tray).difference(".")) == NUMBEROFRECTS


# number of distinct labels is equal to number of distinct tiles
def isInvalid(tray):
    for label in LABELS:
        if 0 < tray.count(label) != LABELS[label]:
            return True
    return False


# Given the last block, Check if block is overlapping with other blocks, or has dimensions outside the puzzle
# This can be done in the solve routine to not choose positions that will go out of bounds
def bruteForce(tray):
    if isInvalid(tray):
        return ""
    if isSolved(tray):
        return tray
    counter = 0
    b = BLOCKS[0]
    while b[2] in tray:
        counter += 1
        b = BLOCKS[counter]
    choices = choosePos(tray, b)
    for choice in choices:
        newTray = placeBlock(tray,choice)
        bF = bruteForce(newTray)
        if bF:
            return bF
    return ""

def choosePos(tray, b):
    choices = []
    for row in range(HEIGHT):
        for col in range(WIDTH):
            pos = row * WIDTH + col
            if tray[pos] == ".":
                if pos // WIDTH == (pos + b[0]-1) // WIDTH and (pos + (b[1]-1) * WIDTH) < TRAYAREA:
                    choices.append((pos,b[0],b[1],b[2]))
                if pos // WIDTH == (pos + b[1]-1) // WIDTH and (pos + (b[0]-1) * WIDTH) < TRAYAREA:
                    choices.append((pos,b[1],b[0],b[2]))
    return choices
def placeBlock(tray,b):
    newTray = list(tray)
    pos = b[0]
    for i in range(b[2]):
        for j in range(b[1]):
            newTray[pos+(i*WIDTH)+j] = b[3]
    return "".join(newTray)

# Check isSolved and isInvalid
# Choose left hand corner of next available block
# Return label of block for isInvalid
def printformat(tray):
    global HEIGHT,WIDTH
    if tray == "":
        print("No Solution")
        return
    dec = []
    pos = 0
    cols = ["" for i in range(WIDTH)]
    for i in range(TRAYAREA):
        cols[i%WIDTH] += tray[i]
    tray = "".join(cols)
    posSet = set()
    WIDTH,HEIGHT = HEIGHT,WIDTH
    for i in range(HEIGHT):
        print(tray[i*WIDTH:i*WIDTH+WIDTH])
    while pos < TRAYAREA:
        if pos not in posSet:
            sym = tray[pos]
            w = 0
            while pos//WIDTH == (pos + w) //WIDTH and tray[pos+w] == sym:
                w += 1
            h = 0
            while pos+(h*WIDTH) < TRAYAREA and tray[pos+(h*WIDTH)] == sym:
                h += 1
            for i in range(h):
                for j in range(w):
                    posSet.add(pos + (i * WIDTH) + j)
            dec.append(str(h)+"x"+str(w))
        pos += 1
    print("Decomposition: " + " ".join(dec))


l = sys.argv[1:]
ints = [int(n) for n in " ".join(l).lower().replace("x", " ").split(" ")]
rects = [(ints[i], ints[i + 1]) for i in range(0, len(ints), 2)]
setLookups(rects)
if isImpossible(rects):
    print("No Solution")
else:
    printformat(bruteForce("." * WIDTH * HEIGHT))

# General Comments
# At start sort blocks by length
