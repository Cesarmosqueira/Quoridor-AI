from collections import deque
from copy import deepcopy
def win_condition(board):
    if 'O' in board[-2]: return 'O'
    if 'X' in board[1]: return 'X'
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
def get_next_move(board, side, startpoint): ## side == True = UP else DOWN 
    dx = [1, -1, 0, 0] ## R L D U
    dy = [0, 0, 1, -1]
               #       (UR UL DR DL)
    diagonals = [(-1,1), (-1,-1), (1,1), (1,-1)]
    n, m = len(board), len(board[0])
    if side:
        original = deepcopy(board[-1])
        for i in range(len(board[-1])): board[-1][i][0] = 'W'
    else: 
        original = deepcopy(board[0])
        for i in range(len(board[0])): board[0][i][0] = 'W'

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
        print("wtf")
        return -1, -1
    
    while len(q):
        r, c = q.popleft()
        if board[r][c][0] == 'W':
            for i in board: print(i)
            if side: board[-1] = original
            else: board[0] = original
            return reconstruct_path(r,c)
            break
        print("Posible moves from ", (r,c))
        for i in board[r][c][1]:
            print("\t- ",(dy[i],dx[i]))
            nr, nc = r + dy[i], c + dx[i]
            if valid(nr, nc):
                if board[nr][nc][0] == 'X' or board[nr][nc][0] == 'O':    
                    if(valid(nr+dy[i],nc+dx[i])):
                        q.append((nr+dy[i],nc+dx[i]))
                        move_reg[nr+dy[i]][nc+dx[i]] = i+4
                    else:
                        pass
                        #      (UR UL DR DL)
                        #  (-1,1), (-1,-1), (1,1), (1,-1)
                        """
                        print("found a diagonal movement", end = " ")
                        if dy[i] == 0:
                            if valid(r+dx[i],c+1):      
                                q.append((r+dx[i],c+1))  
                                move_reg[r+dx[i]][c+1] = 8 + (0 if dx[i] == -1 else 2)

                            if valid(r+dx[i],c-1):      
                                q.append((r+dx[i],c-1))    
                                move_reg[r+dx[i]][c-1] = 8 + (1 if dx[i] == -1 else 3)

                        if dx[i] == 0:
                            if valid(r+1,c+dy[i]): 
                                q.append((r+1,c+dy[i]))
                                move_reg[r+1][c+dy[i]] = 8 + (3 if dy[i] == -1 else 2)

                            if valid(r-1,c+dy[i]): 
                                q.append((r-1,c+dy[i]))
                                move_reg[r-1][c+dy[i]] = 8 + (1 if dy[i] == -1 else 0)
                        """
                else:
                    move_reg[nr][nc] = i
                    q.append((nr, nc))
       

    print("WTF")
    return -1,-1



