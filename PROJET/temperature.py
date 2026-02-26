"""
02/06/2025
@bastien.rossiaud

"""
import multiprocessing as mp
import os
import time
import random

def Controleur(mem_t,mem_p,seuil_T,seuil_P,ver,x,go_pompe,go_chauffage):
    """
    Fonction de contrôle qui active ou désactive la pompe et le chauffage selon les seuils.

    Entrées :
        mem_t (mp.Value) : Valeur partagée de la température.
        mem_p (mp.Value) : Valeur partagée de la pression.
        seuil_T (float) : Seuil de température à ne pas dépasser.
        seuil_P (float) : Seuil de pression à ne pas dépasser.
        ver (mp.Lock) : Verrou pour la synchronisation des accès mémoire.
        x (float) : Temps d'attente entre chaque contrôle (en secondes).
        go_pompe (mp.Value) : Variable partagée pour l'état de la pompe (True/False).
        go_chauffage (mp.Value) : Variable partagée pour l'état du chauffage (True/False).

    Sorties :
        Aucune (modifie les variables partagées go_pompe et go_chauffage).
    """
    while True :
        with ver:
            T=mem_t.value
            P=mem_p.value
            go_chauffage.value = T<=seuil_T
            go_pompe.value = P<=seuil_P

        time.sleep(x) #simule la répétition toutes les X secondes avec le while True

def Temperature(ver, mem_t,s):
    """
    Génère une température aléatoire et la stocke dans la mémoire partagée.

    Entrées :
        ver (mp.Lock) : Verrou pour la synchronisation des accès mémoire.
        mem_t (mp.Value) : Valeur partagée de la température.
        s (float) : Temps d'attente entre chaque génération (en secondes).

    Sorties :
        Aucune (modifie la variable partagée mem_t).
    """
    while True:
        T = round(random.uniform(15,25),2)
        with ver : 
            mem_t.value=T
        time.sleep(s)

def Pression(ver, mem_p, u):
    """
    Génère une pression aléatoire et la stocke dans la mémoire partagée.

    Entrées :
        ver (mp.Lock) : Verrou pour la synchronisation des accès mémoire.
        mem_p (mp.Value) : Valeur partagée de la pression.
        u (float) : Temps d'attente entre chaque génération (en secondes).

    Sorties :
        Aucune (modifie la variable partagée mem_p).
    """
    while True :
        P = round(random.uniform(0.5,1.5),2)
        with ver : 
            mem_p.value=P
        time.sleep(u)

def Chauffage(z, queue_temp, go_chauffage):
    """
    Indique l'état du chauffage (allumé ou éteint) et l'envoie dans la mémoire partagée.

    Entrées :
        z (float) : Temps d'attente entre chaque vérification (en secondes).
        queue_temp (mp.Queue) : File pour transmettre l'état du chauffage.
        go_chauffage (mp.Value) : Variable partagée pour l'état du chauffage (True/False).

    Sorties :
        Aucune (ajoute un message dans la file queue_temp).
    """
    while True:
        if go_chauffage.value :
            msg = "Chauffage : Allumé"
        else : 
            msg = "Chauffage : éteint"
        queue_temp.put(msg)
        time.sleep(z)

def Pompe(z, queue_pression, go_pompe):
    """
    Indique l'état de la pompe (allumée ou éteinte) et l'envoie dans une file.

    Entrées :
        z (float) : Temps d'attente entre chaque vérification (en secondes).
        queue_pression (mp.Queue) : File pour transmettre l'état de la pompe.
        go_pompe (mp.Value) : Variable partagée pour l'état de la pompe (True/False).

    Sorties :
        Aucune (ajoute un message dans la file queue_pression).
    """   
    while True:
        if go_pompe.value :
            msg = "pompe : Allumée"
        else : 
            msg = "pompe : éteinte"
        queue_pression.put(msg)
        time.sleep(z)

def Ecran(ver, queue_temp, queue_pression, mem_t, mem_p):
    """
    Affiche la température, la pression et l'état des équipements à l'écran.

    Entrées :
        ver (mp.Lock) : Verrou pour la synchronisation des accès mémoire.
        queue_temp (mp.Queue) : File contenant l'état du chauffage.
        queue_pression (mp.Queue) : File contenant l'état de la pompe.
        mem_t (mp.Value) : Valeur partagée de la température.
        mem_p (mp.Value) : Valeur partagée de la pression.

    Sorties :
        Aucune (affiche les informations à l'écran).
    """
    while True:
        with ver:
            temp = queue_temp.get()
            pression = queue_pression.get()
            T = round(mem_t.value,2)
            P = round(mem_p.value,2)
        print("Température de ",T,"\n",temp)
        print("Pression de ",P,"\n",pression)
        time.sleep(0.5)

if __name__ == "__main__":
    ver = mp.Lock()
    queue_temp=mp.Queue()
    queue_pression=mp.Queue()

    seuil_T= 20
    seuil_P=1

    go_pompe = mp.Value("b",False)
    go_chauffage=mp.Value("b",False)

    mem_t = mp.Value("f",0)
    mem_p = mp.Value("f",0)

    x=u=s=z=0.5

    proc_temp = mp.Process(target=Temperature, args= (ver,mem_t,s))
    proc_press = mp.Process(target = Pression, args = (ver,mem_p,u))
    proc_chauffage = mp.Process(target = Chauffage, args = (z,queue_temp,go_chauffage))
    proc_pompe = mp.Process(target = Pompe, args = (z,queue_pression,go_pompe))
    proc_ecran = mp.Process(target = Ecran, args = (ver, queue_temp,queue_pression,mem_t,mem_p))
    proc_controleur = mp.Process(target = Controleur, args = (mem_t,mem_p,seuil_T,seuil_P,ver,x,go_pompe,go_chauffage))

    for p in [proc_temp,proc_press,proc_chauffage,proc_pompe,proc_ecran,proc_controleur]:
        p.start()

    for p in [proc_temp,proc_press,proc_chauffage,proc_pompe,proc_ecran,proc_controleur]:
        p.join()
