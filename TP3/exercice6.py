"""
File name       : exercice6.py
Author          : Adélie GIBOU
Date            : 2025-05-19
Description     : Modification du programme exercice5.py pour qu'il fasse son affichage dans une boucle
conditionnée par une variable booléenne fin initialisée à False et qui sera mise à True par la fonction
d'interception du signal. 
"""



import signal
import time

# Variable globale pour contrôler la boucle
fin = False

# Fonction appelée quand on reçoit SIGINT (Ctrl+C)
def gerer_sigint(signum, frame):
    global fin
    print("\n🔔 SIGINT reçu : on demande l'arrêt du programme.")
    fin = True  # On demande à la boucle de s’arrêter

# Lier SIGINT à la fonction
signal.signal(signal.SIGINT, gerer_sigint)

print("🟢 Programme en cours. Appuyez sur Ctrl+C pour demander l’arrêt proprement.")

# Boucle conditionnée par la variable fin
while not fin:
    print("⏳ Je travaille toujours...")
    time.sleep(1)

print("🛑 Programme terminé proprement après réception de SIGINT.")
