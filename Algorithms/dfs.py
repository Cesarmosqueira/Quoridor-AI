
def solve():
    # movimientos 
    # mov 1: (dx[0], dy[0]) -> (x+1, y)
    # mov 2: (dx[1], dy[0]) -> (x-1, y)
    # ....
    dx = [1,-1,0,0]
    dy = [0,0,1,-1]
    n, m = [int(x) for x in input().split()]
    matriz = [[] for i in range(n)]
    for i in range(n):
        matriz[i] = list(input())
    vis = [[False for i in range(m)] for j in range(n)]

    def valid(row, col):
        return (row >= 0) and (row < n) and (col >= 0) and (col < m) \
            and (matriz[row][col] == '.') and (not vis[row][col])

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
            if (matriz[i][j] == '.') and (not vis[i][j]):
                rooms += 1
                dfs(i, j)
    return rooms

print(solve())
