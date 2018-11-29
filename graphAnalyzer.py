import random
import dbscan_tes
import PageRank
import networkx as nx
import matplotlib.pyplot as plt
from time import time
import fa2
import numpy as np


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
    print(len(set(pr)))

    # ----------------------------------- Clustering Computation --------------------------------------

    forceatlas2 = fa2.ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=0,

        # Performance
        jitterTolerance=.01,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=1,
        strongGravityMode=True,
        gravity=200,
        # Log
        verbose=True)

    pos = forceatlas2.forceatlas2_networkx_layout(G,
                                                  pos=None,
                                                  iterations=300);

    pos = {key: np.array([elt[0], elt[1]]) for key, elt in pos.items()}

    pos_transf = dbscan_tes.transf(pos)  # changing position format to be able to use it in DBSCAN

    clusters = dbscan_tes.dbscan(pos_transf, 24, 16)

    cluster_with_pr = associatingPageRankToNode(pr, clusters)

    # sorting each cluster according to page rank result
    for key in cluster_with_pr.keys():
        cluster_with_pr[key] = sorted(cluster_with_pr[key], key=lambda item: (item[1], item[0]))

    # list of 2-uples containing the highest page rank node from each cluster
    highest_pr_per_cluster = [cluster_with_pr[key][0] for key in cluster_with_pr.keys()]

    # sorting this list by page rank
    highest_pr_per_cluster = sorted(highest_pr_per_cluster, key=lambda item: (item[1], item[0]))

    for elt in highest_pr_per_cluster:
        print(list(G.nodes())[elt[0]], " page rank : ", elt[1])

    # ----------------------------------- Graph Creation --------------------------------------

    # each node within a cluster have the same color
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))

    colors = get_colors(len(clusters.keys()) + 1)
    node_color = ['black' for _ in range(len(G.nodes()))]
    for key, value in clusters.items():
        for elt in value:
            node_color[elt] = colors[key]

    nx.draw(G.to_undirected(), pos, node_size=2, width=.05, edge_color='grey', node_color=node_color)
    plt.savefig("graph_with_layout.png")

    plt.figure()

    node_color = ['blue' for _ in range(len(G.nodes()))]
    node_color[0] = 'red'
    nx.draw(G.to_undirected(), node_color=node_color, node_size=2, width=.05, edge_color='grey')
    plt.savefig("graph_without_layout.png")


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
    containing node index from this cluster and its page rank"""
    cluster_with_pr = {}

    for key, value in cluster.items():
        cluster_with_pr[key] = [(node, pr[node]) for node in value]

    return cluster_with_pr


if __name__ == "__main__":
    top = time()
    graphAnalyzer("network_depth_2.gml")
    print(time() - top)
