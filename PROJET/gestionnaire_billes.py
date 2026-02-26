"""
File name       : gestionnaire_billes.py
Author          : Adélie GIBOU
Date            : 2025-06-02
Description     : Gestionnaire de Billes
"""
import multiprocessing as mp
import os, time, math, random, sys, ctypes, signal


def travailleur(k_bills, m, verrou, nbr_disponible_billes, sem_attente):
    for i in range (m):
        demander(k_bills, verrou, nbr_disponible_billes, sem_attente)
        time.sleep(k_bills)
        rendre(k_bills, verrou, nbr_disponible_billes, sem_attente)

def demander(k_bills, verrou, nbr_disponible_billes, sem_attente):
    verrou.acquire()
    while nbr_disponible_billes.value < k_bills : 
        verrou.release()
        sem_attente.acquire()
        verrou.acquire()
    nbr_disponible_billes.value -= k_bills
    print(f"Fonction demander : {k_bills} pris, reste {nbr_disponible_billes.value}")
    verrou.release()
    
def rendre(k_bills, verrou, nbr_disponible_billes, sem_attente):
    with verrou :
        nbr_disponible_billes.value += k_bills
        print(f"Fonction rendre : {k_bills} rendu, total {nbr_disponible_billes.value}")
    sem_attente.release()

def controleur(max_billes, verrou, nbr_disponible_billes, stop_event):
    while not stop_event.is_set():
        with verrou :
            nb = nbr_disponible_billes.value
            if 0 <= nb <= max_billes:
                print(f"Tout va bien!")
            else :
                print(f"Erreur")
        time.sleep(1)


if __name__ == "__main__" :
    nb_process_travailleur = 4
    process_travailleur = [0 for i in range (nb_process_travailleur)]
    k_bills = [4, 3, 5, 2]
    m = 3
    max_billes = 9
    verrou = mp.Lock()
    sem_attente = mp.Semaphore(0)

    nbr_disponible_billes = mp.Value('i', max_billes)

    stop_event = mp.Event()
    
    for i in range(nb_process_travailleur):
        process_travailleur[i] = mp.Process(target=travailleur, args=(k_bills[i], m, verrou, nbr_disponible_billes, sem_attente))
        process_travailleur[i].start()
        
    process_controleur = mp.Process(target=controleur, args=(max_billes, verrou, nbr_disponible_billes, stop_event))
    process_controleur.start()
    
    time.sleep(1)
    
    for i in range(nb_process_travailleur):
        process_travailleur[i].join()

    stop_event.set()
    process_controleur.join()