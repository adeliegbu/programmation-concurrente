"""
File name       : course_hippique.py
Author          : Adélie GIBOU
Date            : 2025-06-02
Description     : Course hippique avec affichage à l'écran (réalisation de la fonction arbitre)
To do           : Dessiner un cheval, pas de dessin graphique !!
"""

# Course Hippique (version élèves)
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Quelques codes d’échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H" # Clear SCReen
CLEAREOS = "\x1B[J" # Clear End Of Screen
CLEARELN = "\x1B[2K" # Clear Entire LiNe
CLEARCUP = "\x1B[1J" # Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH" # (’H’ ou ’f’) : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K" # effacer après la position du curseur
CRLF = "\r\n" # Retour à la ligne

# VT100 : Actions sur le curseur
CURSON = "\x1B[?25h" # Curseur visible
CURSOFF = "\x1B[?25l" # Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m" # Normal
BOLD = "\x1B[1m" # Gras
UNDERLINE = "\x1B[4m" # Souligné

# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m" # Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m" # Rouge
CL_GREEN="\033[22;32m" # Vert
CL_BROWN = "\033[22;33m" # Brun
CL_BLUE="\033[22;34m" # Bleu
CL_MAGENTA="\033[22;35m" # Magenta
CL_CYAN="\033[22;36m" # Cyan
CL_GRAY="\033[22;37m" # Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m" # Gris foncé
CL_LIGHTRED="\033[01;31m" # Rouge clair
CL_LIGHTGREEN="\033[01;32m" # Vert clair
CL_YELLOW="\033[01;33m" # Jaune
CL_LIGHTBLU= "\033[01;34m" # Bleu clair
CL_LIGHTMAGENTA="\033[01;35m" # Magenta clair
CL_LIGHTCYAN="\033[01;36m" # Cyan clair
CL_WHITE="\033[01;37m" # Blanc

#−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
import multiprocessing as mp
import os, time, math, random, sys, ctypes, signal

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')
                              
def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !
def erase_line() : print(CLEARELN,end='')

lock = mp.Lock()
                         
# La tache d’un cheval
def un_cheval(ma_ligne : int, keep_running, lock) : # ma_ligne commence à 0
    """
    Représente un cheval qui avance ligne par ligne dans la course.

    Args:
        ma_ligne (int): index du cheval (définit la ligne où il s'affiche)
        keep_running (mp.Value): variable partagée pour savoir si la course continue
        lock (mp.Lock): verrou pour éviter les conflits d'affichage
    """
    col=1
    while col < LONGEUR_COURSE and keep_running.value :
        move_to(ma_ligne+1,col) # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        with lock:
            print(chr(ord('A') + ma_ligne) + "//\\\\")

        positions[ma_ligne] = col

        col+=1
        time.sleep(0.1 * random.randint(1,5))

    keep_running.value=False

def arbitre(positions, keep_running, Nb_process, pari_utilisateur, lock):
    """
    Arbitre qui observe les positions des chevaux en temps réel et annonce le(s) gagnant(s), perdant(s), ainsi que le résultat du pari utilisateur.

    Args:
        positions (mp.Array): tableau partagé des positions des chevaux
        keep_running (mp.Value): indique si la course est encore en cours
        Nb_process (int): nombre total de chevaux en course
        pari_utilisateur (str): lettre correspondant au cheval parié par l'utilisateur
        lock (mp.Lock): verrou pour l'affichage
    """
    while keep_running.value:
        time.sleep(0.1)
        positions_list = list(positions)
        premier = max(positions_list)
        dernier = min(positions_list)

        move_to(Nb_process+3, 1)
        erase_line()
        prems = []
        for i in range(Nb_process):
            if positions_list[i] == premier:
                prems.append(chr(ord('A')+i))
        en_rouge()
        with lock:
            print(f"En tête : ",' '.join(prems))
        
        move_to(Nb_process+4, 1)
        erase_line()
        dern = []
        for i in range(Nb_process):
            if positions_list[i] == dernier:
                dern.append(chr(ord('A')+i))
        en_rouge()
        with lock:
            print(f"Dernier(s) :",' '.join(dern))

    
    if not keep_running.value :
        move_to(Nb_process+3, 1)        
        erase_line()
        if len(prems)==1:
            with lock:
                print(f"Vainqueur : {' '.join(prems)}")
        else:
            with lock:
                print(f"Vainqueurs ex aequos :",' '.join(prems))
                    
        move_to(Nb_process+4, 1)
        erase_line()
        if len(dern)==1:
            with lock:
                print(f"Perdant : {' '.join(dern)}")            
        else:
            with lock:
                print(f"Perdants ex aequos :",' '.join(dern))

        move_to(Nb_process+5, 1)  
        if pari_utilisateur in prems: 
            with lock:
                print(f"Bravo! Le cheval {pari_utilisateur} a gagné la course!")
        else:
            with lock:
                print(f"Dommage, le cheval {pari_utilisateur} n'a pas gagné la course...")

#−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def detourner_signal(signum, stack_frame):
    """
    Fonction appelée en cas d'interruption (Ctrl+C).
    Affiche un message et termine proprement le programme.

    Args:
        signum (int): numéro du signal
        stack_frame: état de la pile au moment du signal
    """
    move_to(Nb_process+2, 1)            # Nb_process est une variable globale
    erase_line()
    move_to(Nb_process+2, 1)

    curseur_visible()
    with lock:
        print("La course est interrompu ...")
    exit(0)
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# La partie principale :
if __name__ == "__main__" :

                            
    LONGEUR_COURSE = 50 # Tout le monde aura la même copie (donc no need to have a ’value’)
    keep_running=mp.Value(ctypes.c_bool, True)

    Nb_process=20
    mes_process = [0 for i in range(Nb_process)]

    positions = mp.Array('i', [0] * Nb_process)

    effacer_ecran()
    curseur_invisible()

    # Détournement d’interruption
    signal.signal(signal.SIGINT, detourner_signal) # CTRL_C_EVENT ?

# Pari ----------------------------------------------
    print("Chevaux en course :")
    print(' '.join([f"{chr(ord('A') + i)}" for i in range(Nb_process)]))

    # Demande à l'utilisateur sur qui il parie
    pari_utilisateur = input("Pariez sur un cheval (ex: A, B, C...) : ").upper()
    essais_pari = 0
    while not (len(pari_utilisateur) == 1 and 'A' <= pari_utilisateur < chr(ord('A') + Nb_process)):
        essais_pari += 1
        pari_utilisateur = input("Choix invalide. Pariez sur un cheval valide : ").upper()

    for i in range(1, 4 + essais_pari):  # lignes 1 à 4 plus le nombre d'essais de pari que le joueur a fait s'il s'est trompé en pariant sur un cheval invalide
        move_to(i, 1)
        erase_line()
# ---------------------------------------------------

    for i in range(Nb_process): # Lancer Nb_process processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,lock,))
        mes_process[i].start()

    arbitre_process = mp.Process(target=arbitre, args=(positions, keep_running, Nb_process, pari_utilisateur, lock,))
    arbitre_process.start()


    move_to(Nb_process+8, 1)
    print("tous lancés, CTRL−C arrêtera la course ...")

    for i in range(Nb_process): mes_process[i].join()

    arbitre_process.join()

    move_to(Nb_process+7, 1)
    curseur_visible()