def solucion_p1(vs):
    d= [(1,0), (0, 1)]
    m, n = len(vs), len(vs[0])
    p = [[(-1,-1) for _ in range(n)]for _ in range(m)]
    def valid(r, c): return 0 <= r and r < m and 0 <= c and c < n

    c = np.zeros((len(vs), len(vs[0])), np.int64)
    c.fill(np.sum(vs)+1)
    c[0][0] = vs[0][0]
    for i in range(m):
        for j in range(n):
            w = c[i][j]
            for dy, dx in d:
                nr, nc = i+dy, j+dx
                if valid(nr, nc):
                    if p[nr][nc] == (-1, -1):
                        p[nr][nc] = (i,j)
                    new_cost = vs[nr][nc]+c[i][j]
                    if new_cost < c[nr][nc]:
                        c[nr][nc] = new_cost
                        p[nr][nc] = (i,j)

    def get_mov(r,col): ## S o E 
        nr, nc = p[r][col]
        if r == nr: return "E"
        if col == nc: return "S"
        else: raise Exception("error")
    r, col = m-1, n-1
    res = ""
    while((r,col) != (0,0)):
        res += get_mov(r,col) + "-"
        r, col = p[r][col]

    return res[::-1], c[m-1][n-1]

