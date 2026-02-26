"""
Filename: exercice5.py
Author: Adélie Gibou
Date: 12 may 2025
Description: 
"""

import os,sys,time

if len(sys.argv) != 2:
    print("Il faut entrer un argument")
    sys.exit(1)

try:
    N = sys.argv[1]
except ValueError:
    print("L'argument doit être un entier")
    sys.exit(1)

for i in range (1, N+1):
    pid_fils = os.fork()
    if pid_fils == 0 :
        print(f"mon pid : {os.getpid()}, celui de mon père : {os.getppid()}")
        time.sleep(2*i)
        print(f"Fin de l'attente de {2*i} secondes")
        sys.exit(i)

for i in range (N):
    pid_terminé, etat = os.wait()
    