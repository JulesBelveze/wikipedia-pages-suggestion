import numpy as np


class PageRank:

    def __init__(self, graph):
        self.__graphNodes = list(graph.nodes())
        self.__lenGraph = len(graph.nodes())
        self.__M = np.zeros((self.__lenGraph, self.__lenGraph))
        self.__V = np.array([1 / self.__lenGraph] * self.__lenGraph)

    def constructDispersionMatrix(self, graph):
        for edge in graph.edges():
            i = self.__graphNodes.index(edge[0])
            j = self.__graphNodes.index(edge[1])
            self.__M[i][j] = 1

        sum_col = np.sum(self.__M, axis=0)
        sum_col[sum_col == 0] = 1
        self.__M = self.__M / sum_col

    def getPageRank(self):
        return np.dot(self.__M, self.__V)

    def getDispersionMatrix(self):
        return self.__M

    def getVector(self):
        return self.__V
