"""
File name       : estimation_pi_monoprocess.py
Author          : Adélie GIBOU
Date            : 2025-06-02
Description     : Estimation de pi par la méthode Mono-Processus
"""

import random, time
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            count += 1
    return count

if __name__ == "__main__" :
    nb_total_iteration = 10000000 # Nombre d’essai pour l’estimation

    debut = time.time()

    nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration)
    
    pi = 4 * nb_hits / nb_total_iteration
    
    fin = time.time()
    duree = fin - debut

    print(f"Valeur estimée de Pi par la méthode Mono−Processus : {pi}")
    print(f"Temps de calcul par la méthode Mono-Processus : {duree} secondes")