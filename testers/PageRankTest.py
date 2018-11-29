import networkx as nx
import sys
sys.path.append('..')
import PageRank

G = nx.DiGraph()

G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11])

G.add_edge(1,2)
G.add_edge(1,4)
G.add_edge(1,3)
G.add_edge(2,3)
G.add_edge(4,3)
G.add_edge(1,5)
G.add_edge(2,1)
G.add_edge(5,2)
G.add_edge(3,4)
G.add_edge(2,4)

PR = PageRank.PageRank(G)
PR.constructDispersionMatrix(G)
print(PR.getPageRank())
print(sum(PR.getPageRank()))