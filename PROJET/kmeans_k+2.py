"""
File name       : kmeans_parallel.py
Author          : Adélie GIBOU
Date            : 2025-06-16
Description     : Algorithme K-means généralisé pour k>2
"""

import random
import math
import multiprocessing as mp

def distance(p1, p2):
    return math.dist(p1, p2)

def moyenne(points):
    if not points:
        return [0, 0]
    x_total = sum(p[0] for p in points)
    y_total = sum(p[1] for p in points)
    return [x_total / len(points), y_total / len(points)]

def centroid_init(X, k):
    centres = [random.choice(X)]
    while len(centres) < k:
        max_dist = -1
        next_centre = None
        for point in X:
            if point in centres:
                continue
            min_dist = min(distance(point, c) for c in centres)
            if min_dist > max_dist:
                max_dist = min_dist
                next_centre = point
        centres.append(next_centre)
    return centres

def assigner_points_aux_clusters(args):
    X_chunk, centres = args
    clusters = [[] for _ in centres]
    for point in X_chunk:
        dists = [distance(point, c) for c in centres]
        index = dists.index(min(dists))
        clusters[index].append(point)
    return clusters

def fusionner_clusters(liste_de_clusters):
    k = len(liste_de_clusters[0])
    fusion = [[] for _ in range(k)]
    for clusters in liste_de_clusters:
        for i in range(k):
            fusion[i].extend(clusters[i])
    return fusion

def K_means_parallele(nb_points, k, epsilon=0.1, max_iter=100):
    X = [[random.randint(0, 100), random.randint(0, 100)] for _ in range(nb_points)]
    centres = centroid_init(X, k)

    for _ in range(max_iter):
        cpu_count = mp.cpu_count()
        taille = len(X) // cpu_count
        morceaux = [X[i * taille:(i + 1) * taille] for i in range(cpu_count)]
        if len(X) % cpu_count != 0:
            morceaux[-1].extend(X[cpu_count * taille:])

        with mp.Pool() as pool:
            resultats = pool.map(assigner_points_aux_clusters, [(chunk, centres) for chunk in morceaux])

        clusters = fusionner_clusters(resultats)
        nouveaux_centres = [moyenne(c) for c in clusters]

        if all(distance(a, b) < epsilon for a, b in zip(centres, nouveaux_centres)):
            break
        centres = nouveaux_centres

    return clusters, centres


if __name__ == "__main__":
    clusters, centres = K_means_parallele(100, 3)
    for i, c in enumerate(centres):
        print(f"Centre {i+1} : {c}")
