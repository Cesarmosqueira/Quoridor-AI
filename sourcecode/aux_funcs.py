from collections import deque
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
def get_next_move(board, side, startpoint, D): ## side == True = UP else DOWN 
    dx = [1, -1, 0, 0] ## R L D U
    dy = [0, 0, 1, -1]
              #       (UR UL DR DL)
              #  (-1,1), (-1,-1), (1,1), (1,-1)
    diagonals = [(-1,1), (-1,-1), (1,1), (1,-1)]
    n, m = len(board), len(board[0])
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
        distcount = 0
        while move_reg[r][c] >= 0:
            distcount += 1
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
                return distcount if D else last 
            else: last = [r-1,c-1]
        
        print("---")
        return -1, -1
    
    while len(q):
        r, c = q.popleft()
        if board[r][c][0] == 'W':
            ## 0 = L
            ## 1 = T
            ## 2 = R
            ## 3 = B
            if side == 1: board[-1] = original
            elif side == 3: board[0] = original
            elif side == 0: 
                for i in range(len(board)):
                    board[i][-1] = original[i]
            elif side == 2: #right
                for i in range(len(board)):
                    board[i][0] = original[i]
            return reconstruct_path(r,c)
        for i in board[r][c][1]:
            nr, nc = r + dy[i], c + dx[i]
            if valid(nr, nc):
                if board[nr][nc][0] in 'L T R B'.split():    
                    if(valid(nr+dy[i],nc+dx[i]) and i in board[nr][nc][1]):
                        q.append((nr+dy[i],nc+dx[i]))
                        move_reg[nr+dy[i]][nc+dx[i]] = i+4
                    else:
                        #      (UR UL DR DL)
                        #  (-1,1), (-1,-1), (1,1), (1,-1)
                        if dy[i] == 0: ##r o l
                            if valid(r+1, c+dx[i]) and 2 in board[r][c+dx[i]][1]: #d
                                q.append((r+1,c+dx[i]))
                                move_reg[r+1][c+dx[i]] = 8 + (3 if dx[i] == -1 else 2) 
                            if valid(r-1, c+dx[i]) and 3 in board[r][c+dx[i]][1]: #u
                                q.append((r-1,c+dx[i]))
                                move_reg[r-1][c+dx[i]] = 8 + (1 if dx[i] == -1 else 0) 
                        
                        if dx[i] == 0: ##u o d
                            if valid(r+dy[i], c-1) and 1 in board[r+dy[i]][c][1]: #l
                                q.append((r+dy[i], c-1)) 
                                move_reg[r+dy[i]][c-1] = 8 + (1 if dy[i] == -1 else 3)

                            if valid(r+dy[i], c+1) and 0 in board[r+dy[i]][c][1]: #r
                                q.append((r+dy[i], c+1)) 
                                move_reg[r+dy[i]][c+1] = 8 + (0 if dy[i] == -1 else 2)
                else:
                    move_reg[nr][nc] = i
                    q.append((nr, nc))
       
    for i in board: print(i)
    print("---")
    return -1,-1


def should_move(board, players, cp):
    dist = [-1 for _ in range(4)]
    for p in players:
        dist[p.side] = get_next_move(board, p.side, (p.y+1, p.x+1), True)
    return dist[cp] == max(dist), dist


def minimax(board, turn, p):
    
    p[turn].place_fence(board, 
    minimax(board,(turn + 1)%4, players) 
    return
    
        

def where_to_place(board, side, players):
    return




















