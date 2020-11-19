from collections import deque


mat = [  ['#','#','#','#','#','#','#'],
         ['#',' ','#','A','#','B','#'],
         ['#',' ',' ',' ','#',' ','#'],
         ['#',' ','#',' ','#',' ','#'],
         ['#',' ','#','#','#',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#','#','#','#','#','#','#']]

n, m = len(mat), len(mat[0])


start, end = (-1,-1), (-1,-1)
for i in range(n):
    for j in range(m):
        if mat[i][j] == 'A':
            start = (i, j)
        if mat[i][j] == 'B':
            end = (i, j)

p = [[-1 for i in range(m)] for j in range(n)] # path
# -2 si (i, j) es 'A'
# -1 si no ha sido visitado
# 0..3 si lo he visitado, su valor es el ultimo mov que hice para llegar
dx = [1,-1,0,0]
dy = [0,0,1,-1]
dd = list("DURL") # enumerar los movimientos

def valid(x, y):
    return (x >= 0) and (x < n) and (y >= 0) and (y < m) and (mat[x][y] != '#') \
        and (p[x][y] == -1)

def recontruir_camino():
    x, y = end
    path = deque()
    while (x, y) != start:
        i = p[x][y]
        path.appendleft(dd[i])
        x -= dx[i]
        y -= dy[i]
        mat[x][y] = '+' if (x,y) != start else 'A'
    print('YES')
    print(len(path))
    print(''.join(path))

q = deque([start])
p[start[0]][start[1]] = -2

while len(q) > 0:
    x, y = q.popleft()
    if (x, y) == end:
        recontruir_camino()
        break
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if valid(nx, ny):
            p[nx][ny] = i 
            q.append((nx, ny))
print('NO')
for i in mat:
    print(i)