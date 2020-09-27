h, w = [int(x) for x in input().split()]
board = []
for i in range(h):
    board.append(list(input()))
vis = [[False]*w]*w
directions = [(1,0),(-1,0),(0,1),(0,-1)]

def valid(r,c):
    return 0 <= r and r < h and 0 <= c and c < w and board[r][c] != '#' \
           and not vis[r][c]
    
def dfs(r,c):
    vis[r][c] = True
    for d in directions:
        nr, nc = r+d[0], c+d[1]
        if valid(nr,nc):
            dfs(nr,nc)


c = 0
for i in range(h):
    for j in range(w):
        if valid(i,j):
            dfs(i,j)
            c+=1

if c > 1:
    print("Invalid board")
