import Fifo
import WikiPagesReader
import hashingTable
import depthController
import networkx as nx
import matplotlib.pyplot as plt


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
        depthC.cursorUpdate()
        links_current_url = WikiPagesReader.wikiPagesFinder(current_url)  # computing all mentionned pages

        # removing all url already in fifo
        links_current_distinct_url = []
        for url in links_current_url:
            if hashT.add(url):  # return True if url not in hashing table
                links_current_distinct_url.append(url)

        if depthC.depthControl():
            fifo.addList(links_current_distinct_url)  # add all the element mentionned in the current fifo
            depthC.addElementsToTreat(links_current_distinct_url)

        G.add_node(current_url)
        G.add_nodes_from(links_current_distinct_url)

        for elt in links_current_distinct_url:
            G.add_edge(current_url,
                       elt)  # adding edge from current_url to elt (because elt is mentionned in current_url
    plt.rcParams["figure.figsize"] = (5,10)
    nx.draw(G, node_size = 2, width=.3)
    plt.show()


if __name__ == "__main__":
    graphConstructor(
        "http://en.wikipedia.org/w/api.php/?action=query&titles=England&prop=revisions&rvprop=timestamp|content&format=json&rvdir=older&rvstart=2018-09-25T00:00:00Z&rvend=2017-01-03T00:00:00Z&rvlimit=1",
        1)
