import networkx as nx


def dist(G, node1, node2):
    if node1 == node2:
        return 0
    else:
        try:
            return nx.shortest_path_length(G, source=node1, target=node2)
        except nx.exception.NetworkXNoPath:
            return 1000


def neigh(node, eps, data, G):
    close_points = []
    for i in range(len(data)):
        if float(dist(G, node, data[i])) <= eps:  # time conumption can be optimize
            close_points.append(i)

    return close_points


def dbscan(G, eps, minPts):
    data = list(G.nodes())
    cluster = 0  # counting clusters
    dico_clusters = {}
    dico_visit = {}  # unvisit if not visited
    for i in range(len(data)):
        dico_visit[i] = 'unvisited'

    for i in range(len(data)):
        if dico_visit[i] == 'unvisited':
            neighbours = neigh(data[i], eps, data, G)
            if len(neighbours) < minPts:
                dico_visit[i] = 'noise'
            else:
                cluster += 1
                dico_clusters[cluster] = expand(i, neighbours, eps, minPts, dico_visit, data, G)
    # print(dico_visit)
    return dico_clusters


def expand(i, neighbours, eps, minPts, dico_visit, data, G):
    cluster = [i]  # create a set if problems with distinct elmt
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

            neighbours_z = neigh(data[index], eps, data, G)

            if len(neighbours_z) >= minPts:
                neighbours = neighbours + neighbours_z
        i += 1

    return cluster
