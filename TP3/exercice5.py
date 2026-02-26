"""
File name       : exercice5.py
Author          : Adélie GIBOU
Date            : 2025-05-19
Description     : Modification du programme exercice4.py pour qu'il ignore le signal SIGINT.
"""



import signal
import time

# On ignore le signal SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal.SIG_IGN)

print("Programme lancé. Ctrl+C sera ignoré.")

while True:
    print("⏳ Je travaille encore...")
    time.sleep(1)
