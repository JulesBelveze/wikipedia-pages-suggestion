import numpy as np
import random


def kmeans(data, nb_clusters, delta, max_iter=1000):
    """kmeans(dqtq, nb_clusters, delta, max_iter=1000) performs the clustering of the data (list of array) using
    the Kmeans algorithm and return a dictionary which has the number of the cluster as a key and the index
    of the nodes that are in the clusters as a value
    Arguement:
    data is the data to cluster, list of array
    nb_clusters is the number of clusters the user want the program to return, int
    delta is the stop criteria that will be compared the maximum distance between the centroids in iteration i and
    the centroids in iteration i-1, float
    max_iter(=1000 by default) is the maximum iterations possible"""
    n = len(data)
    nb_iter = 0

    # Initializing randomly the centers of the clusters
    try:
        centers = [data[i] for i in random.sample(range(n), int(nb_clusters))]
    except ValueError:
        print("Not enough data for that number of clusters")

    stability = 20  # Initializing the stability to a high value
    while stability > delta and nb_iter < max_iter:
        # Update of the centers
        centers1 = centroids(data, centers)
        centers = centers1

        # Update of the difference between i and i-1
        stability = stabilityBtw(centers, centers1)

        nb_iter += 1

    # Creation of the dico of clusters to have the good output for graph analyzer
    dico_cluster = {key: [] for key in range(len(centers))}
    for i in range(n):
        dico_cluster[cluster(data[i], centers)].append(i)

    return dico_cluster


def dist(x, y):
    """compute the euclidean distance between x and y"""
    return np.linalg.norm(x - y)


def cluster(x, centers):
    """return the cluster index in centers of x"""
    distances = [dist(x, y) for y in centers]
    min_dist = distances[0]
    min_index = 0
    for i in range(1, len(distances)):
        if distances[i] < min_dist:
            min_dist = distances[i]
            min_index = i
    return min_index


def cent(S):
    """return the centroid of the set S of data"""
    return sum(S) / len(S)


def centroids(data, centers):
    """return the centroids of the clusters"""
    clusters = [[] for _ in range(len(centers))]
    for elmt in data:
        clusters[cluster(elmt, centers)].append(elmt)

    centers1 = [cent(elmt) for elmt in clusters]
    return centers1


def stabilityBtw(centers, centers1):
    """return the max distance between to list of points"""
    distances = [dist(x, y) for x, y in zip(centers, centers1)]
    return max(distances)
