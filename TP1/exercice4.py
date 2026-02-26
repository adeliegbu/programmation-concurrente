"""
Filename: exercice4.py
Author: Adélie Gibou
Date: 05 may 2025
Description: 
"""

import os, sys
N = 4

# 1
for i in range(1, N + 1):
    pid = os.fork()
    if pid == 0:
        # Processus enfant
        print(f"Je suis le processus {os.getpid()}, mon père est le processus {os.getppid()}")
    else:
        # Processus parent -> on stoppe pour que seul l’enfant continue la chaîne
        os.wait()  # Attend son enfant avant de terminer
        sys.exit()

# 2
for i in range(1, N + 1):
    pid = os.fork()
    if pid == 0:
        print(f"Je suis le processus {os.getpid()}, mon père est le processus {os.getppid()}")
        sys.exit()