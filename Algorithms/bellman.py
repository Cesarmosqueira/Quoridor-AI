
n, m = map(int, input().split())
ed = [] # lista de aristas
for i in range(m):
    x, y, w = map(int, input().split())
    ed.append((x, y, w))

inf = 10**18
d = [inf] * n
d[0] = 0

for i in range(n):
    for u,v,w in ed:
        if d[u] > inf and d[u] + w < d[v]:
            d[v] = d[u] + w

print(d)
