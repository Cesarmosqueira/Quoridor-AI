import numpy as np

col, row = 3,3

board = []

for i in range(0,row*2+1):
	board.append([{True:'.', False:'o'} [i%2==0 or x%2==0] for x in range(col*2+1)])

print(np.array(board))

