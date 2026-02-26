"""
File name       : exercice2.py
Author          : Adélie GIBOU
Date            : 2025-05-19
Description     : Ecriture de 2 scripts Python réalisant respectivement les 2 commandes composées suivantes :
* cat fichier | wc
* sort < fichier | grep chaine | tail –n 5 > sortie
"""



# cat fichier | wc
fichier = "exercice2.txt"

with open(fichier, "r", encoding="utf-8") as f:
    contenu = f.read()
lignes = contenu.count("\n") + 1 if contenu else 0
mots = len(contenu.split())
caractres = len(contenu)

print(lignes, mots, caractres)



# sort < fichier | grep chaine | tail –n 5 > sortie
fichier = "exercice2.txt"
chaine = "toto"
fichier_sortie = "sortie.txt"

with open(fichier, "r", encoding="utf-8") as f:
    lignes = f.readlines()

lignes_triees = sorted(lignes)

filtrees = [ligne for ligne in lignes_triees if chaine in ligne]

dernieres = filtrees[-5:]

with open(fichier_sortie, "w", encoding="utf-8") as f:
    f.writelines(dernieres)

print(f"Résultat écrit dans {fichier_sortie}")