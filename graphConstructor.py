import Fifo
import WikiPagesReader
import hashingTable
import DBSCAN
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

    nx.write_gml(G, "network_depth_3.gml")
    nx.draw(G, node_size=2, width=.3, edge_color=colors)
    plt.savefig("graph.png")


def graphLoader(path):
    G = nx.read_gml(path)
    G = removeIsolatedNodes(G)
    
    G.remove_node(list(G.nodes)[0])
    print(DBSCAN.dbscan(G, 1, 2))
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, node_size=2, width=.3)
    # plt.show()

# function removing all nodes that are targeted only once and which are not targeting anyone
def removeIsolatedNodes(G):
    node_list = list(G.nodes())
    for node in node_list:
        if (len(G.out_edges(node)) == 0) and (len(G.in_edges(node)) == 1):
            G.remove_node(node)

    return G


if __name__ == "__main__":
    top = time()
    # graphConstructor(
    #     "http://en.wikipedia.org/w/api.php/?action=query&titles=Asbel_Kiprop&prop=revisions&rvprop=timestamp|content&format=json&rvdir=older&rvstart=2018-09-25T00:00:00Z&rvend=2017-01-03T00:00:00Z&rvlimit=1",
    #     2)
    graphLoader("network_depth_2.gml")
    print(time() - top)
