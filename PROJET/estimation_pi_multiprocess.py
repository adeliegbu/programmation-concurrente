"""
File name       : estimation_pi_multiprocess.py
Author          : Adélie GIBOU
Date            : 2025-06-02
Description     : Estimation de pi par la méthode Multi-Processus
"""

import multiprocessing as mp
import os, time, math, random, sys, ctypes, signal

def frequence_de_hits_pour_n_essais(nb_iteration, queue):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        if x *x + y *y <= 1:
            count += 1
    queue.put(count)

if __name__ == "__main__" :
    nb_total_iteration = 10000000 # Nombre d’essai pour l’estimation
    nb_process = 16
    nb_iteration_par_process = nb_total_iteration // nb_process

    queue = mp.Queue()
    process = [0 for i in range (nb_process)]

    debut = time.time()

    for i in range(nb_process):
        process[i] = mp.Process(target=frequence_de_hits_pour_n_essais, args=(nb_iteration_par_process, queue))
        process[i].start()

    for i in range(nb_process):
        process[i].join()

    total_hits = 0
    for i in range (nb_process):
        total_hits += queue.get()
    
    pi = 4 * total_hits / nb_total_iteration

    fin = time.time()
    duree = fin - debut

    print(f"Valeur estimée de Pi par la méthode Multi-Processus : {pi}")
    print(f"Temps de calcul par la méthode Multi-Processus : {duree} secondes")