"""
Filename: exercice2.py
Author: Adélie Gibou
Date: 12 may 2025
Description: 
"""
import os,sys

for i in range(3):
    p = os.fork()
    valeur_de_i = i
    pid = os.getpid()
    ppid = os.getppid()
    print(f"(i : {valeur_de_i}) je suis le processus : {pid}, mon père est : {ppid}, retour : {p}")
sys.exit()