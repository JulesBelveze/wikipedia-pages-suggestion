# DBSCAN

import numpy as np


def transf(pos):
    data = []
    for key, value in pos.items():
        data.append([key, value])

    return data


def dist(x, y):
    return np.linalg.norm(x - y)


# function finding all the points that belong to a circle of center x and radius eps
def neigh(x, eps, data):
    close_points = []
    for i in range(len(data)):
        if float(dist(x, data[i][1])) <= eps:
            close_points.append(i)
    return close_points


# main function of the DBSCAN algorithm
def dbscan(data, eps, minPts):
    cluster = 0  # counting clusters
    dico_clusters = {}
    dico_visit = {}  # unvisit if not visited
    for i in range(len(data)):
        dico_visit[i] = 'unvisited'

    for i in range(len(data)):
        if dico_visit[i] == 'unvisited':
            neighbours = neigh(data[i][1], eps, data)
            if len(neighbours) < minPts:
                dico_visit[i] = 'noise'
            else:
                cluster += 1
                dico_clusters[cluster] = expand(i, neighbours, eps, minPts, dico_visit, data)

    invert_dico_cluster = {}
    for clu, list_index in dico_clusters.items():
        for elmt in list_index:
            invert_dico_cluster[elmt] = clu

    return dico_clusters


# function that expands a given cluster
def expand(i, neighbours, eps, minPts, dico_visit, data):
    cluster = [i]
    dico_visit[i] = 'core'
    i = 0
    while i < len(neighbours):
        index = neighbours[i]
        if dico_visit[index] == 'noise':
            dico_visit[index] = 'core'
            cluster.append(index)

        elif dico_visit[index] == 'unvisited':
            cluster.append(index)
            dico_visit[index] = 'core'
            neighbours_z = neigh(data[index][1], eps, data)

            if len(neighbours_z) >= minPts:
                neighbours = neighbours + neighbours_z
        i += 1

    return cluster
