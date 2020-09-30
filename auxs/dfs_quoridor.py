
matriz = [['#','#','#','#','#','#','#'],
         ['#',' ','#','2','#',' ','#'],
         ['#',' ','#',' ','#',' ','#'],
         ['#',' ','#',' ','#',' ','#'],
         ['#',' ','#','#','#',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ','1',' ',' ','#'],
         ['#','#','#','#','#','#','#']]



dx = [1,-1,0,0]
dy = [0,0,1,-1]
n, m = len(matriz), len(matriz[0])


vis = [[False for i in range(m)] for j in range(n)]

def valid(row, col):
    return (row >= 0) and (row < n) and (col >= 0) and (col < m) \
        and (matriz[row][col] != '#') and (not vis[row][col])

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
        if (matriz[i][j] != '#') and (not vis[i][j]):
            rooms += 1
            dfs(i, j)
print(rooms)