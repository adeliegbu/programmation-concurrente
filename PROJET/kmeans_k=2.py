"""
File name       : kmeans.py
Author          : Adélie GIBOU
Date            : 2025-06-02
Description     : Algorithme de K-means
"""

import multiprocessing as mp
import os, time, math, random, sys, ctypes, signal

def moyenne(points):
    if not points:
        return [0, 0]
    x_total = sum([p[0] for p in points])
    y_total = sum([p[1] for p in points])
    n = len(points)
    return [x_total / n, y_total / n]

def SSE(L, centre):
    return sum(math.dist(p, centre)**2 for p in L)

def choisir_centres(liste, k, nb_points):
    centres = []
    while len(centres) < k:
        option = liste[random.randint(0, nb_points - 1)]
        if option not in centres:
            centres.append(option)
    return centres

def assigner_points(liste, centres):
    clusters = [[] for _ in centres]
    for point in liste:
        distances = [math.dist(point, c) for c in centres]
        index_min = distances.index(min(distances))
        clusters[index_min].append(point)
    return clusters

def K_means(nb_points, epsilon, k):
    liste = []
    for i in range(nb_points):
        liste.append([random.randint(0, 100), random.randint(0, 100)])

    centres = choisir_centres(liste, k, nb_points)

    clusters = assigner_points(liste, centres)
    m_1 = moyenne(clusters[0])
    m_2 = moyenne(clusters[1])
    old_m1 = m_1[:]
    old_m2 = m_2[:]

    fini = False
    while not fini:
        clusters = assigner_points(liste, [m_1, m_2])
        L_1 = clusters[0]
        L_2 = clusters[1]

        m_1 = moyenne(L_1)
        m_2 = moyenne(L_2)

        if math.dist(old_m1, m_1) < epsilon and math.dist(old_m2, m_2) < epsilon:
            fini = True
        else:
            old_m1 = m_1[:]
            old_m2 = m_2[:]

    return L_1, L_2, m_1, m_2

L1, L2, m1, m2 = K_means(100, 0.1, 2)
print(m1, m2)