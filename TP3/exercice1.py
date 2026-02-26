"""
File name       : exercice1.py
Author          : Adélie GIBOU
Date            : 2025-05-19
Description     : Réalisation d'un script montrant l’utilisation d’un tube anonyme (pipe) entre deux processus.
"""


import os , sys
msg = "monMessage"
print ("Création d’un pipe anonyme")
(dfr , dfw) = os.pipe()
n = os.write(dfw , msg.encode()) #je dépose msg dans le tube
print ("Le processus %d a transmis le message %s\n" %(os.getpid() , msg ) )
msgRecu = os.read(dfr , len(msg)).decode()
print ("Le processus %d a reçu le message %s\n" %(os.getpid() , msgRecu))
os.close(dfr) ; os.close(dfw)
sys.exit(0)