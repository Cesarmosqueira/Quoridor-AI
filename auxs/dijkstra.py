import game
import heapq as hp

# rows, cols = 9
# board = game.Board(rows,cols, screen)

inf = 10**18

n, m = map(int, input().split())
vs = [[] for i in range(board.rows)]

for i in range(board.rows):
	x, y, w = map(int, input().split())
	x -= 1
	y -= 1
	#Grafo dirigido
	vs[x].append((w, y)) # Par (peso, nodo)

# Hallar el camino más corto desde el nodo 1 hasta todos los demás
# Para nosotros, es el nodo 0

q = [(0, 0)] #Puedo llegar al nodo 0 con distancia 0
vis = [False] * board.rows
d = [inf] * board.rows #d[i]: Mejor distancia que conozco para llegar a 'i'
d[0] = 0

#La cola de prioridad contiene pares (distancia, nodo)
while len(q) > 0:
	_, v = hp.heappop(q)
	if vis[v]: continue
	vis[v] = True
	for w, e in vs[v]:
		if (not vis[e]) and d[v] + w < d[e]:
			d[e] = d[v] + w
			hp.heappush(q, (d[e], e))

for i in range(board.rows):
	print(d[i], end=' ')