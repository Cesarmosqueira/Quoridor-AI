from collections import deque

def win_condition(board):
    if 'O' in board[-1]: return 'O'
    elif 'X' in board[1]: return 'X'
    if 'B' in board[-1]: return 'B'
    elif 'A' in board[1]: return 'A'
    else: return ' '

def valid_block(board, r, c):
    board[r][c] = '#'
    dx = [1,-1,0,0]
    dy = [0,0,1,-1]
    n, m = len(board), len(board[0])

    vis = [[False for i in range(m)] for j in range(n)]

    def valid(row, col):
        return (row >= 0) and (row < n) and (col >= 0) and (col < m) \
            and (board[row][col] != '#') and (not vis[row][col])

    def dfs(row, col):
        vis[row][col] = True
        for i in range(4):
            nx = row + dx[i]
            ny = col + dy[i]
            if valid(nx, ny):
                dfs(nx, ny)

    rooms = 0

    for i in range(n):
        for j in range(m):
            if (board[i][j] != '#') and (not vis[i][j]):
                rooms += 1
                dfs(i, j)
    
    board[r][c] = ' '
    return rooms == 1

mat =   [['#','#','#','#','#','#','#'],
         ['#',' ','#','X','#',' ','#'],
         ['#',' ',' ',' ','#',' ','#'],
         ['#',' ','#',' ','#',' ','#'],
         ['#',' ','#','#','#',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ','O',' ',' ','#'],
         ['#','#','#','#','#','#','#']]


dx = [1, -1, 0, 0] ## R L D U
dy = [0, 0, 1, -1]
           #       (UR UL DR DL)
diagonals = [(-1,1), (-1,-1), (1,1), (1,-1)]

def get_next_move(board, side, startpoint): ## side == True = UP else DOWN 
    n, m = len(board), len(board[0])
    if side:
        original = board[-1]
        board[-1] = ['W' if board[-1][x] == ' ' or board[-1][x] == '#' else board[-1][x] for x in range(m)]
    else: 
        original = board[0]
        board[0] = ['W' if board[0][x] == ' ' or board[0][x] == '#' else board[0][x] for x in range(m)]

    q = deque([startpoint])
    move_reg = [[-1 for y in range(m)] for x in range(n)] 
    

    def valid(row, col):
        return 0 <= row and row < n and 0 <= col and col < m and move_reg[row][col] == -1 and board[row][col] != '#'

    def reconstruct_path(r, c):
        last = [r,c]
        while move_reg[r][c] >= 0:
            i = move_reg[r][c] 
            if i < 4:
                r -= dx[i]
                c -= dy[i]
            elif i < 8:
                print(i)
                r -= 2*dx[i%4]
                c -= 2*dy[i%4]
            else: 
                i %= 4
                r -= diagonals[i][0]
                c -= diagonals[i][1]
            if (r,c) == startpoint:
                return last
            else: last = [r-1,c-1]
        print("wtf")
        return -1, -1
            
    while len(q):
        r, c = q.popleft()
        if board[r][c] == 'W':
            print(move_reg[r][c])
            if side: board[-1] = original
            else: board[0] = original
            return reconstruct_path(r,c)
            break
        for i in range(4):
            nr, nc = r + dx[i], c + dy[i]
            if valid(nr, nc):
                if board[nr][nc] == 'X' or board[nr][nc] == 'O' or board[nr][nc] == 'B' or board[nr][nc] == 'A':    
                    if(valid(nr+dx[i],nc+dy[i])):
                        print("Im doing douyblke at", board[nr+dx[i]][nc+dy[i]])
                        q.append((nr+dx[i],nc+dy[i]))
                        move_reg[nr+dx[i]][nc+dy[i]] = i+4
                    else:
                        #      (UR UL DR DL)
                        #  (-1,1), (-1,-1), (1,1), (1,-1)
                        if dx[i] == 0:
                            if valid(r+dy[i],c+1):      
                                q.append((r+dy[i],c+1))  
                                move_reg[r+dy[i]][c+1] = 8 + (0 if dy[i] == -1 else 2)

                            if valid(r+dy[i],c-1):      
                                q.append((r+dy[i],c-1))    
                                move_reg[r+dy[i]][c-1] = 8 + (1 if dy[i] == -1 else 3)

                        if dy[i] == 0:
                            if valid(r+1,c+dx[i]): 
                                q.append((r+1,c+dx[i]))
                                move_reg[r+1][c+dx[i]] = 8 + (3 if dx[i] == -1 else 2)

                            if valid(r-1,c+dx[i]): 
                                q.append((r-1,c+dx[i]))
                                move_reg[r-1][c+dx[i]] = 8 + (1 if dx[i] == -1 else 0)

                else:
                    move_reg[nr][nc] = i
                    q.append((nr, nc))
       

    print("WTF")
    return -1,-1



