# Inner Hexagon 7 8 9 14 15 16
# H1 0 1 2 6 7 8
# H2 2 3 4 8 9 10
# H3 5 6 7 12 13 14
# H4 9 10 11 16 17 18
# H5 13 14 15 19 20 21
# H6 15 16 17 21 22 23
import sys
def hextodict(puzzle):
    hexlook = {0: [puzzle[7], puzzle[8], puzzle[9], puzzle[14], puzzle[15], puzzle[16]],
               1: [puzzle[0], puzzle[1], puzzle[2], puzzle[6], puzzle[7], puzzle[8]],
               2: [puzzle[2], puzzle[3], puzzle[4], puzzle[8], puzzle[9], puzzle[10]],
               3: [puzzle[5], puzzle[6], puzzle[7], puzzle[12], puzzle[13], puzzle[14]],
               4: [puzzle[9], puzzle[10], puzzle[11], puzzle[16], puzzle[17], puzzle[18]],
               5: [puzzle[13], puzzle[14], puzzle[15], puzzle[19], puzzle[20], puzzle[21]],
               6: [puzzle[15], puzzle[16], puzzle[17], puzzle[21], puzzle[22], puzzle[23]]}
    return hexlook


def hextorows(puzzle):
    hexlook = {0: [puzzle[0], puzzle[1], puzzle[2], puzzle[3], puzzle[4]],
               1: [puzzle[5], puzzle[6], puzzle[7], puzzle[8], puzzle[9], puzzle[10], puzzle[11]],
               2: [puzzle[12], puzzle[13], puzzle[14], puzzle[15], puzzle[16], puzzle[17], puzzle[18]],
               3: [puzzle[19], puzzle[20], puzzle[21], puzzle[22], puzzle[23]],
               4: [puzzle[0], puzzle[1], puzzle[6], puzzle[5], puzzle[12]],
               5: [puzzle[3], puzzle[2], puzzle[8], puzzle[7], puzzle[14], puzzle[13], puzzle[19]],
               6: [puzzle[4], puzzle[10], puzzle[9], puzzle[16], puzzle[15], puzzle[21], puzzle[20]],
               7: [puzzle[11], puzzle[18], puzzle[17], puzzle[23], puzzle[22]],
               8: [puzzle[5], puzzle[12], puzzle[13], puzzle[19], puzzle[20]],
               9: [puzzle[0], puzzle[6], puzzle[7], puzzle[14], puzzle[15], puzzle[21], puzzle[22]],
               10: [puzzle[1], puzzle[2], puzzle[8], puzzle[9], puzzle[16], puzzle[17], puzzle[23]],
               11: [puzzle[3], puzzle[4], puzzle[10], puzzle[11], puzzle[18]]
               }
    return hexlook


def isInvalid(hexlook={},switch = 0):
    for key in hexlook:
        for i in range(1, 7+ switch, 1):
            if hexlook[key].count(str(i)) > 1:
                return True
    return False


def isSolved(puzzle):
    hexl = hextodict(puzzle)
    return [*puzzle].count(".") == 0 and not isInvalid(hexl)


def solve(puzzle, type = "A"):
    switch = 0
    if type == "A":
        hexl = hextodict(puzzle)
    if type == "B":
        hexl = hextorows(puzzle)
        switch = 1
    if isInvalid(hexl,switch):
        return ""
    if isSolved(puzzle):
        return puzzle
    i = puzzle.find(".")
    for j in range(1, 7+switch, 1):
        puzzle = puzzle[:i] + str(j) + puzzle[i + 1:]
        #print(puzzle)
        bF = solve(puzzle,type)
        if bF:
            return bF
    return "No Solution"

def printformat(puzzle):
    print()
    print(" " + puzzle[:5] + " ")
    print(puzzle[5:12])
    print(puzzle[12:19])
    print(" " + puzzle[19:] + " ")

l = sys.argv
# print(solve("123456.....61.....154321"))
if len(l) == 2:
    printformat(l[1])
    printformat(solve(l[1]))
if len(l) == 3:
    printformat(solve(l[2],l[1]))

#print(hextorows("123121456451263123624546"))
