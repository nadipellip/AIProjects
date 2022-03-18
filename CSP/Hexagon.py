# Inner Hexagon 7 8 9 14 15 16
# H1 0 1 2 6 7 8
# H2 2 3 4 8 9 10
# H3 5 6 7 12 13 14
# H4 9 10 11 16 17 18
# H5 13 14 15 19 20 21
# H6 15 16 17 21 22 23
def hextodict(puzzle):
    hexlook = {1: [puzzle[2], puzzle[5], puzzle[8]], 2: [puzzle[1], puzzle[3], puzzle[10]], 3: [puzzle[2], puzzle[4],
                                                                                                puzzle[14]],
               4: [puzzle[3], puzzle[5], puzzle[12]], 5: [puzzle[1], puzzle[4], puzzle[6]],
               6: [puzzle[5], puzzle[7], puzzle[11]], 7: [puzzle[6], puzzle[8], puzzle[18]],
               8: [puzzle[1], puzzle[7], puzzle[9]], 9: [puzzle[8], puzzle[10], puzzle[17]],
               10: [puzzle[2], puzzle[9], puzzle[15]], 11: [puzzle[6], puzzle[12], puzzle[19]],
               12: [puzzle[4], puzzle[11], puzzle[13]], 13: [puzzle[12], puzzle[14], puzzle[20]],
               14: [puzzle[3], puzzle[13], puzzle[15]], 15: [puzzle[10], puzzle[14], puzzle[16]],
               16: [puzzle[15], puzzle[17], puzzle[20]], 17: [puzzle[9], puzzle[16], puzzle[18]],
               18: [puzzle[7], puzzle[17], puzzle[19]], 19: [puzzle[11], puzzle[18], puzzle[20]],
               20: [puzzle[13], puzzle[16], puzzle[19]]}
    return hexlook


def isInvalid(hexlook={}):
    for key in hexlook:
        for i in range(1, 7, 1):
            if hexlook[key].count(str(i)) > 1:
                return True
    return False


def isSolved(puzzle):
    hexl = hextodict(puzzle)
    return [*puzzle].count(".") == 0 and not isInvalid(hexl)


def solve(puzzle):
    hexl = hextodict(puzzle)
    if isInvalid(hexl):
        return ""
    if isSolved(puzzle):
        return puzzle
    i = puzzle.find(".")
    for j in range(1, 7, 1):
        puzzle = puzzle[:i] + str(j) + puzzle[i + 1:]
        bF = solve(puzzle)
        if bF:
            return bF


def printformat(puzzle):
    print("Puzzle:" + puzzle)
    print(" " + puzzle[:5] + " ")
    print(puzzle[5:12])
    print(puzzle[12:19])
    print(" " + puzzle[19:] + " ")


# print(solve("123456.....61.....154321"))
sol = solve()
# printformat(solve("........................"))
# print(isSolved("123121456451263123624546"))
isSolved("6")
