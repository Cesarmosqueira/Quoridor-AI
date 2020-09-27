from collections import deque
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

n, m = [int(x) for x in input().split()] 

board = [[] for x in range(n)] 

start, end = (-1, -1), (-1, -1)
for i in range(n):
	board[i] = list(input())
	for j in range(m):
		if board[i][j] == 'A':
			start = (i, j)
		if board[i][j] == 'B':
			end = (i, j)


move_reg = [[-1 for y in range(m)] for x in range(n)] 

move_reg[start[0]][start[1]] = -2
q = deque([start])

def valid(row, col):
	return 0 <= row and row < n and 0 <= col and col < m and board[row][col] != '#' and move_reg[row][col] == -1

def bfs():
	flag = False
	while len(q):
		r, c = q.popleft()
		if (r, c) == end:
			reconstruct_path()
			flag = True
			break
		for i in range(4):
			nr, nc = r + dx[i], c + dy[i]
			if valid(nr, nc):
				move_reg[nr][nc] = i
				q.append((nr, nc))

	if not flag: print("No suitable path")
	else:
		for i in board: print(i)

def reconstruct_path():
	r, c  = end
	while move_reg[r][c] >= 0:
		i = move_reg[r][c] 
		r -= dx[i]
		c -= dy[i]
		board[r][c] =  'A' if board[r][c] == 'A' else '+'

bfs()