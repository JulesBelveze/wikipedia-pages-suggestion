import Fifo
import WikiPagesReader
import hashingTable
import random
import dbscan_tes
import PageRank
import depthController
import networkx as nx
import matplotlib.pyplot as plt
from time import time


def graphConstructor(wikiInput, stop):
    fifo = Fifo.Fifo()
    hashT = hashingTable.UrlDistinctTester()
    depthC = depthController.DepthController(stop)
    fifo.addElement(wikiInput)

    G = nx.DiGraph()  # creating direct graph

    while not (fifo.isFifoEmpty()):
        # handling fifo
        current_url = fifo.removeFirstIn()  # extracting elt to use
        print(current_url)
        depthC.elementsTreated()
        print(depthC.getCursor(), depthC.getTable())
        links_current_url = WikiPagesReader.wikiPagesFinder(current_url)  # computing all mentionned pages

        if depthC.depthControl() == 1:
            # removing all url already in fifo
            links_current_distinct_url = []
            for url in links_current_url:
                if hashT.add(url):  # return True if url not in hashing table
                    links_current_distinct_url.append(url)

            fifo.addList(links_current_distinct_url)
            depthC.addElementsToTreat(links_current_distinct_url)

            G.add_node(current_url)
            G.add_nodes_from(links_current_distinct_url)

            for elt in links_current_url:
                G.add_edge(current_url,
                           elt,
                           color='b')  # adding edge from current_url to elt (because elt is mentionned in current_url

        # when going through last layer's nodes
        elif depthC.depthControl() == 2:
            edges_to_add = [elt for elt in links_current_url if hashT.checkInTable(elt)]
            for elt in edges_to_add:
                G.add_edge(current_url,
                           elt,
                           color='g', )  # adding edge from current_url to elt (because elt is mentionned in current_url

        depthC.cursorUpdate()

    print(len(G.nodes()))
    plt.rcParams["figure.figsize"] = (5, 10)
    colors = [G[u][v]['color'] for u, v in G.edges()]

    nx.write_gml(G, "network_depth_2.gml")
    nx.draw(G, node_size=2, width=.3, edge_color=colors)
    plt.savefig("graph.png")


def graphLoader(path):
    G = nx.read_gml(path)
    G = removeIsolatedNodes(G)
    G.remove_node(list(G.nodes)[0])

    pr = PageRank.PageRank(G)
    pr.constructDispersionMatrix(G)
    pr = pr.getPageRank()

    pos = nx.kamada_kawai_layout(G)
    pos_transf = dbscan_tes.transf(pos)

    clusters = dbscan_tes.dbscan(pos_transf, 0.07, 10)
    # cluster_with_pr = associatingPageRankToNode(pr, clusters)
    # for key in cluster_with_pr.keys():
    #     cluster_with_pr[key] = sorted(cluster_with_pr[key], key=lambda item: (item[1], item[0]))

    # each node within a cluster have the same color
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    colors = get_colors(len(clusters.keys()) + 1)
    node_color = ['black' for _ in range(len(G.nodes()))]
    for key, value in clusters.items():
        for elt in value:
            node_color[elt] = colors[key]

    # node size according to node degree
    node_size = []
    for i in (G.nodes()):
        node_size.append(G.degree(i))
    print(node_size)

    nx.draw(G, pos, node_size=1, width=0, edge_color='grey', node_color=node_color, arrows=False)
    # plt.show()
    plt.savefig("graph2.png")


# function removing all nodes that are targeted only once and which are not targeting anyone
def removeIsolatedNodes(G):
    node_list = list(G.nodes())
    for node in node_list:
        if (len(G.out_edges(node)) == 0) and (len(G.in_edges(node)) == 1):
            G.remove_node(node)
    return G


# function returning a dictionnary with key the cluster number and values a list of 2-uples
# containing node index and its page rank
def associatingPageRankToNode(pr, cluster):
    cluster_with_pr = {}

    for key, value in cluster.items():
        cluster_with_pr[key] = [(node, pr[node]) for node in value]

    return cluster_with_pr


if __name__ == "__main__":
    top = time()
    # graphConstructor(
    #     "http://en.wikipedia.org/w/api.php/?action=query&titles=England&prop=revisions&rvprop=timestamp|content&format=json&rvdir=older&rvstart=2018-09-25T00:00:00Z&rvend=2017-01-03T00:00:00Z&rvlimit=1",
    #     1)
    graphLoader("network_depth_2.gml")
    print(time() - top)
