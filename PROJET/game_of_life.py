"""
02/06/2025
@bastien.rossiaud
"""


import multiprocessing as mp
import os
import random
import time

def init_grille(lignes, colonnes):
    grille = []
    for i in range(lignes):
        ligne = []
        for j in range(colonnes):
            ligne.append(random.randint(0,1))
        grille.append(ligne)
    return grille

def voisins(grille,lignes, colonnes, x, y):
    count = 0
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy==0:
                continue
            nouveau_x = x+dx
            nouveau_y = y+dy
            if 0 <= nouveau_x < lignes and 0 <= nouveau_y < colonnes :
                count += grille[nouveau_x][nouveau_y]
    return count

def calcul_ligne(grille, indice_ligne,lignes,colonnes, resultat_liste):
    resultat_ligne=[]
    for i in range(colonnes):
        vivante = grille[indice_ligne][i]
        nb_voisins = voisins(grille,lignes, colonnes, indice_ligne, i)
        if vivante : 
            if nb_voisins < 2 or nb_voisins > 3:
                resultat_ligne.append(0)
            else:
                resultat_ligne.append(1)
        else:
            if nb_voisins == 3 :
                resultat_ligne.append(1)
            else : 
                resultat_ligne.append(0)
    resultat_liste[indice_ligne]=resultat_ligne

def display(grille, ticks):
    print("tick : ", ticks)
    print(f"--- Game of Life : Tick {ticks} ---")
    for ligne in grille : 
        print("".join("█" if cellule else " " for cellule in ligne))

def game_of_life(lignes,colonnes,ticks,delai):
    manager = mp.Manager()
    grille = init_grille(lignes,colonnes)

    for tick in range(ticks):
        display(grille,tick)
        resultat_liste = manager.list()
        for i in range(lignes):
            resultat_liste.append([])
        processus = []

        for i in range(lignes):
            p = mp.Process(target=calcul_ligne, args=(grille,i,lignes, colonnes,resultat_liste))
            p.start()
            processus.append(p)

        for p in processus:
            p.join()
        
        grille = list(resultat_liste)
        time.sleep(delai)

if __name__ == "__main__":
    colonnes, lignes = 15,15
    delai = 0.2
    ticks = 50

    game_of_life(lignes,colonnes,ticks,delai)

