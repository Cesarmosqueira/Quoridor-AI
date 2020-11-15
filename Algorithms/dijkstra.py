n = int(input())
edges = []
for i in range(n):
    edges.append([int(x) for x in input().split()])

start, end = [int(x) for x in input("Start and end ").split()]      

def to_adj(edges, size):
    vs = [[] for _ in range(size)]
    for src, dst, w in edges:
        vs[src].append([dst, w])
    return vs

def dijkstra(vs, start, end):
    cost = [float('inf')]*len(vs)
    parents = [-1]*len(vs)
    cost[start] = 0
    for i in range(len(vs)):
        for e, w in vs[i]:
            if parents[e] == -1:
                parents[e] = i
            new_cost = cost[i]+w
            if cost[e] > new_cost:
                cost[e] = new_cost
                parents[e] = i
    print(parents)
    return cost[end]

adj = to_adj(edges, n)
print("With ", adj, "\n Dijkstra: ", dijkstra(adj, start,end))
