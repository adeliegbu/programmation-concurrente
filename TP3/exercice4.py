"""
File name       : exercice4.py
Author          : Adélie GIBOU
Date            : 2025-05-19
Description     : Ecriture d'un programme qui réalise un affichage dans une boucle infinie, mais qui prévoit de
s'arrêter à la réception du signal SIGINT. La fonction d'interception [de déroutement] affichera un message
signalant la réception du signal avant de terminer le programme par un appel à sys.exit().
"""



import signal
import sys
import time

# Fonction appelée quand le signal SIGINT est reçu
def gerer_sigint(signal, frame):
    print("\n Signal SIGINT reçu (Ctrl+C). Arrêt du programme proprement.")
    sys.exit(0)

# On associe le signal SIGINT à notre fonction
signal.signal(signal.SIGINT, gerer_sigint)

# Boucle infinie
while True:
    print("Le programme tourne... (Ctrl+C pour arrêter)")
    time.sleep(1)


# import signal , sys
# def arreterProgramme(signal, frame) :
#     """Fonction appelée quand vient l'heure d’arrêter notre programme"""
#     print("\n C'est l'heure d’arrêt !")
#     sys.exit(0)
# # Connexion du signal à notre fonction
# signal.signal(signal.SIGINT, arreterProgramme)
# # Notre programme...
# print("Le programme va boucler...")
# while True:
#     continue