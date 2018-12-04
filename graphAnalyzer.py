import dbscan
import PageRank
import Kmeans
import re
import random
import fa2
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from time import time



def graphAnalyzer(graph, kmeans=False):
    """Argument: the path to find a .gml graph file, boolean : if yes using scikit-learn KMean to cluster otherwise
    using our dbscan algorithm.
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

    # constructing network layout
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
                                                  iterations=1000);

    if kmeans:
        # converting positions into a list of np.array
        pos_list = [np.array([elt[0], elt[1]]) for key, elt in pos.items()]

        # clustering the nodes according to the kmeans algorithm
        clusters = Kmeans.kmeans(pos_list, 8, 0.01, 300)

    else:
        pos = {key: np.array([elt[0], elt[1]]) for key, elt in pos.items()}
        pos_transf = dbscan.transf(pos)  # changing position format to be able to use it in DBSCAN
        clusters = dbscan.dbscan(pos_transf, 40, 20)  # clustering

    cluster_with_pr = associatingPageRankToNode(pr, clusters)

    # sorting each cluster according to page rank result
    for key, value in cluster_with_pr.items():
        cluster_with_pr[key] = sorted(value, key=lambda item: (item[1], item[0]))

    # rendering the suggested pages and their page rank
    print("\nThe recommanded pages are the following :")
    for key, value in cluster_with_pr.items():
        try:
            node_index = value[-1][0]  # retrieving the node index
            title_node = re.search(r'titles=(.*?)\&',
                                   list(G.nodes())[node_index])  # getting the title of the Wikipedia page
            print("•", title_node.group(1), "- with a page rank of ", value[-1][1])
        except IndexError:
            pass

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
    kmeans = input(
        "Do you want to use the K-Means algorithm to cluster (True [recommended]/False) ? (if False the DBSCAN algorithm will be used) \n")

    graphAnalyzer("network_depth_2.gml", kmeans)
    print(time() - top)
