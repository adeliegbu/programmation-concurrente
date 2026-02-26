"""
Filename: exercice1.py
Author: Adélie Gibou
Date: 05 may 2025
Description: 
"""

import sys
print("Nom du programme : ", sys.argv[0])
print("Nombre d’arguments : ", len(sys.argv)-1)
print("Les arguments sont : ")
for argument in sys.argv[1:] :
    print(argument)

# je met dans mon terminal : python3 exercice1.py arg1 arg2