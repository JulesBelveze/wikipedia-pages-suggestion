import Fifo
import WikiPagesReader
import hashingTable
import depthController
import networkx as nx
from time import time


def graphConstructor(wikiInput, stop):
    fifo = Fifo.Fifo()
    hashT = hashingTable.UrlDistinctTester()
    depthC = depthController.DepthController(stop)
    fifo.addElement(wikiInput)  # initialization of the fifo

    G = nx.DiGraph()  # creating direct graph

    while not (fifo.isFifoEmpty()):
        # handling fifo
        current_url = fifo.removeFirstIn()  # extracting elt to use
        depthC.elementsTreated()
        links_current_url = WikiPagesReader.wikiPagesFinder(current_url)  # computing all mentionned pages

        if depthC.depthControl() == 1:

            # removing all url already in fifo
            links_current_distinct_url = []
            for url in links_current_url:
                if hashT.add(url):  # return True if url not in hashing table
                    links_current_distinct_url.append(url)

            # feeding the fifo
            fifo.addList(links_current_distinct_url)
            depthC.addElementsToTreat(links_current_distinct_url)

            # feeding the graph
            G.add_node(current_url)
            G.add_nodes_from(links_current_distinct_url)

            # adding edge from current_url to elt (because elt is mentionned in current_url)
            for elt in links_current_url:
                G.add_edge(current_url,
                           elt)

        # when going through last layer's nodes
        elif depthC.depthControl() == 2:
            edges_to_add = [elt for elt in links_current_url if hashT.checkInTable(elt)]
            for elt in edges_to_add:
                G.add_edge(current_url,
                           elt)  # adding edge from current_url to elt (because elt is mentionned in current_url

        depthC.cursorUpdate()

    nx.write_gml(G, "network_depth_2.gml")  # saving the graph into a .gml file


if __name__ == "__main__":
    top = time()
    title = input("About which Wikipedia page do you want to get suggestions ? \n");
    depth = input("What is the depth limit ? (recommended 2)\n")
    graphConstructor(
        "http://en.wikipedia.org/w/api.php/?action=query&titles=" + title + "&prop=revisions&rvprop=timestamp|content&format=json&rvdir=older&rvstart=2018-09-25T00:00:00Z&rvend=2017-01-03T00:00:00Z&rvlimit=1",
        int(depth))
    print(time() - top)
