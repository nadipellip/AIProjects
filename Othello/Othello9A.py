"""
1234
5678
9ABC

CBA9
8765
4321
"""
board = "123456789ABC"
newbrd = [board[len(board)-(i+1)] for i in range(len(board))]
print(board[::-1])
