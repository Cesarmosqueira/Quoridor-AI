import numpy as np

col, row = 3,3

board = [[{True:'#', False:' '}[x==0 or x ==row+1] for x in range(row+2)]]*int(col+2)
a = ['#']*(col+2)
board[0] = a; board[-1] = a

print(np.array(board))

