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


