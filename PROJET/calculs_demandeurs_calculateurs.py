"""
16/06/2025
@bastien.rossiaud
"""

import multiprocessing as mp
import random
import time

def demandeur(id_demandeur, queue_demandes,expressions):
    """
    Fonction qui envoie des expressions à calculer dans une file de demandes.

    Entrées :
        id_demandeur (int) : Identifiant du demandeur.
        queue_demandes (mp.Queue) : File partagée pour envoyer les demandes de calcul.
        expressions (list de str) : Liste des expressions à évaluer.

    Sorties :
        Aucune (les demandes sont ajoutées à la file queue_demandes).
    """
    for expr in expressions:
        queue_demandes.put((id_demandeur, expr))
        time.sleep(random.uniform(0.1, 0.5))

def calculateur(queue_demandes, queue_resultats):
    """
    Fonction qui récupère les demandes de calcul, les évalue et place les résultats dans une file de résultats.

    Entrées :
        queue_demandes (mp.Queue) : File partagée contenant les demandes à traiter (tuple : id_demandeur, expression).
        queue_resultats (mp.Queue) : File partagée pour envoyer les résultats (tuple : id_demandeur, résultat).

    Sorties :
        Aucune (les résultats sont ajoutés à la file queue_resultats).
    """
    while True:
        id_demandeur, expr = queue_demandes.get()
        if expr == "STOP":
            break
        try:
            result = eval(expr)
            queue_resultats.put((id_demandeur, result))
        except:
            queue_resultats.put((id_demandeur, f"Erreur dans l'expression: {expr}"))

def main():
    """
    Fonction principale qui crée les processus demandeurs et calculateurs, gère la synchronisation entre eux,
    puis affiche les résultats obtenus pour chaque demandeur.

    Entrées :
        Aucune.

    Sorties :
        Aucune (affiche les résultats à l'écran).
    """
    m=3
    n=4

    queue_demandes = mp.Queue()
    queue_resultats = mp.Queue()

    expressions = ["2 + 3", "5 * 6", "10 - 4", "16 / 2", "2 + 3 -"]

    liste_demandeurs = []
    for i in range(m):  
        p = mp.Process(target=demandeur, args=(i, queue_demandes,expressions))
        p.start()
        liste_demandeurs.append(p)

    liste_calculateurs = []
    for _ in range(n):
        p = mp.Process(target=calculateur, args=(queue_demandes, queue_resultats))
        p.start()
        liste_calculateurs.append(p)

    for p in liste_demandeurs:
        p.join()

    for _ in range(n): 
        queue_demandes.put((0, "STOP"))

    for p in liste_calculateurs:
        p.join()

    results = {}
    while not queue_resultats.empty():
        id_demandeur, result = queue_resultats.get()
        if id_demandeur not in results:
            results[id_demandeur] = []
        results[id_demandeur].append(result)

    for id_demandeur, results in results.items():
        print(f"Demandeur {id_demandeur} a reçu les résultats: {results}")

if __name__ == "__main__":
    main()
