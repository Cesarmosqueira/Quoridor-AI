from collections import deque
import heapq as hp
from copy import deepcopy
def win_condition(board):
    if 'T' in [c[0] for c in board[-2]]: return 'T'
    if 'B' in [c[0] for c in board[ 1]]: return 'B'
    return ' '

def valid_fence(board):
    dx = [1,-1,0,0]
    dy = [0,0,1,-1]
    n, m = len(board), len(board[0])

    vis = [[False for i in range(m)] for j in range(n)]

    def valid(row, col):
        return (row >= 0) and (row < n) and (col >= 0) and (col < m) \
            and (board[row][col][0] != '#') and (not vis[row][col])

    def dfs(row, col):
        vis[row][col] = True
        for i in board[row][col][1]:
            nc = col + dx[i]
            nr = row + dy[i]
            if valid(nr, nc):
                dfs(nr, nc)

    rooms = 0

    for i in range(n):
        for j in range(m):
            if (board[i][j][0] != '#') and (not vis[i][j]):
                rooms += 1
                if rooms > 1: 
                    print("dfs found more than one room") 
                    return False
                dfs(i, j)

    print("dfs found ", rooms, "rooms") 
    return rooms == 1
####MOVS##### (DX,DY)
#
# [(1,0), (-1,0), (0,1), (0,-1)]
#
#    R       L      D       U
#

        ## 0 = L
        ## 1 = T
        ## 2 = R
        ## 3 = B
def get_next_move(board, side, startpoint): ## side == True = UP else DOWN 
    dx = [1, -1, 0, 0] ## R L D U
    dy = [0, 0, 1, -1]
               #       (UR UL DR DL)
    diagonals = [(-1,1), (-1,-1), (1,1), (1,-1)]
    n, m = len(board), len(board[0])
    print(side)
    if side == 1:
        original = deepcopy(board[-1])
        for i in range(len(board[-1])): board[-1][i][0] = 'W'
    elif side == 3: 
        original = deepcopy(board[0])
        for i in range(len(board[0])): board[0][i][0] = 'W'
    elif side == 0: #left
        original = []
        for i in range(len(board)):
            original.append(deepcopy(board[i][-1]))
            board[i][-1][0] = 'W'
    elif side == 2: #right
        original = []
        for i in range(len(board)):
            original.append(deepcopy(board[i][0]))
            board[i][0][0] = 'W'
    q = deque([startpoint])
    move_reg = [[-1 for y in range(m)] for x in range(n)] 
    
    def valid(row, col):
        return 0 <= row and row < n and 0 <= col and col < m and move_reg[row][col] == -1 and \
                board[row][col][0] != '#'

    def reconstruct_path(r, c):
        last = [r,c]
        while move_reg[r][c] >= 0:
            i = move_reg[r][c] 
            if i < 4:
                r -= dy[i]
                c -= dx[i]
            elif i < 8:
                r -= 2*dy[i%4]
                c -= 2*dx[i%4]
            else: 
                #      (UR UL DR DL)
                #  (-1,1), (-1,-1), (1,1), (1,-1)
                r -= diagonals[i-8][0]
                c -= diagonals[i-8][1]
            if (r,c) == startpoint:
                return last
            else: last = [r-1,c-1]
        
        print("---")
        for i in move_reg: print(i)
        return -1, -1
    
    vs = [[] for _ in range(n)]
    for src, dst, 1 in 
    for i in range(len(board)):
        for e, 1 in vs[i]:




    for i in board: print(i)
    print("---")
    return -1,-1



