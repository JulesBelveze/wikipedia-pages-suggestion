import random
import dbscan_tes
import PageRank
import networkx as nx
import matplotlib.pyplot as plt
from time import time


def graphAnalyzer(graph):
    """Argument: the path to find a .gml graph file
    Will page rank and cluster the nodes in order to return the highest page rank page in the three biggest clusters
    It also print a graph in order to visualize the clustering"""
    G = nx.read_gml(graph)
    G = removeIsolatedNodes(G)  # removing meaningless nodes
    G.remove_node(list(G.nodes)[0])

    # ----------------------------------- PageRank Computation --------------------------------------

    # creating a PageRank object
    pr = PageRank.PageRank(G)
    pr.constructDispersionMatrix(G)
    pr = pr.getPageRank()

    # ----------------------------------- Clustering Computation --------------------------------------

    pos = nx.kamada_kawai_layout(G)
    pos_transf = dbscan_tes.transf(pos)  # changing position format to be able to use it in DBSCAN

    clusters = dbscan_tes.dbscan(pos_transf, 0.07, 10)

    cluster_with_pr = associatingPageRankToNode(pr, clusters)

    # sorting each cluster according to page rank result
    for key in cluster_with_pr.keys():
        cluster_with_pr[key] = sorted(cluster_with_pr[key], key=lambda item: (item[1], item[0]))

    # ----------------------------------- Graph Creation --------------------------------------

    # each node within a cluster have the same color
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))

    colors = get_colors(len(clusters.keys()) + 1)
    node_color = ['black' for _ in range(len(G.nodes()))]
    for key, value in clusters.items():
        for elt in value:
            node_color[elt] = colors[key]

    nx.draw(G, pos, node_size=2, width=.1, edge_color='grey', node_color=node_color, arrows_size=.4)
    # plt.show()
    plt.savefig("graph2.png")


def removeIsolatedNodes(G):
    """function removing all nodes from a graph G that are targeted only once and which are not targeting anyone"""
    node_list = list(G.nodes())
    for node in node_list:
        if (len(G.out_edges(node)) == 0) and (len(G.in_edges(node)) == 1):
            G.remove_node(node)
    return G



def associatingPageRankToNode(pr, cluster):
    """function taking a pagerank results and cluster dictionnary
    and returning a dictionnary with as key the cluster number and values a list of 2-uples
    containing node index and its page rank"""
    cluster_with_pr = {}

    for key, value in cluster.items():
        cluster_with_pr[key] = [(node, pr[node]) for node in value]

    return cluster_with_pr


if __name__ == "__main__":
    top = time()
    graphLoader("network_depth_2.gml")
    print(time() - top)
