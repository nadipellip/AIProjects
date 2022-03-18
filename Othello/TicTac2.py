import sys
def setLookups(inputval):
    global HEIGHT, WIDTH, SIZE, WINCONDITION, CONSTRAINTS,TURN,OPTIONS
    OPTIONS = ("x","o")
    b = inputval[1]
    TURN = OPTIONS[1-(b.count(".")%2)]
    WINCONDITION = 3
    SIZE = len(inputval[1])
    if len(inputval) > 2:
        WIDTH = int(inputval[2])
    else:
        WIDTH = int(SIZE**(0.5)+0.5)
    HEIGHT = SIZE // WIDTH
    CONSTRAINTS = []
    for row in range(HEIGHT):
        for col in range(WIDTH):
            pos = row * WIDTH + col
            if (col + WINCONDITION-1) // WIDTH < 1:
                c = []
                for p in range(WINCONDITION):
                    c.append(pos+p)
                CONSTRAINTS.append(c)
            if (row+WINCONDITION-1) // HEIGHT < 1:
                c = []
                for p in range(WINCONDITION):
                    c.append(pos + WIDTH*p)
                CONSTRAINTS.append(c)
            if (row+WINCONDITION-1) // HEIGHT < 1 and (col + WINCONDITION-1) // WIDTH < 1:
                c = []
                for p in range(WINCONDITION):
                    c.append(pos+WIDTH*p+p)
                CONSTRAINTS.append(c)
            if (row+WINCONDITION-1) // HEIGHT < 1 and (col-WINCONDITION+1) >= 0:
                c = []
                for p in range(WINCONDITION):
                    c.append(pos+WIDTH*p-p)
                CONSTRAINTS.append(c)
def winner(board):
    for c in CONSTRAINTS:
        vals = {board[pos] for pos in c}
        if len(vals) == 1 and "." not in vals:
            return 1 if board[c[0]] == TURN else -1
    if board.count(".") == 0:
        return 0
    return

def minimax(board): #TERMINAL MINIMAX
    #reports scores based on X's point of view(preferred player)
    #determine all moves and classify them tkn is "x" or "o" according to which side is to move
    turn = OPTIONS[1-(board.count(".")%2)]
    term = winner(board)
    print(term)
    if term == 0 or term:
        return {-1: term}#1/-1 for x/o win, 0 for tie
    result = {}     #result {move: board evalutation}
    moves = [idx for idx in range(SIZE) if board[idx] == "."]
    for move in moves:
        newBoard = [*board]
        newBoard[move] = turn
        newBoard = "".join(newBoard)
        mini = minimax(newBoard)
        brdEval = max(mini.values()) if turn == TURN else min(mini.values())
        result[move] = brdEval
    return result
l = sys.argv
setLookups(l[:])
print(TURN)
print(minimax(l[1]))
"""def classifyMoves(board): #TERMINAL MINIMAX
    #reports scores based on X's point of view(preferred player)
    #determine all moves and classify them tkn is "x" or "o" according to which side is to move
    if board is terminal:
        return (-1: board evaluation}#1/-1 for x/o win, 0 for tie
    result = {}     #result {move: board evalutation}
    for move in moves:
        newBoard = board after tkn makes move
        cM = classifyMoves(newBoard)
        brdEval = max(cM.values()) if tkn == "x" else min(cM.values())
        result[move] = brdEval
    return result """