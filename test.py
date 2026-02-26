import os
import sys
import signal
import multiprocessing as mp

def F1(s1, s3):
    k=0
    while(True):
        s1.aquire()
        print("P1 - iteration =", k)
        k += 1
        s3.release()
    sys.exit(0)

def F2(s2, s3):
    k=0
    while(True):
        s2.aquire()
        print("P1 - iteration =", k)
        k += 1
        s3.release()
    sys.exit(0)

def F3(s1, s2, s3):
    k=0
    while(True):
        s3.aquire()
        s3.aquire()
        print("P1 - iteration =", k)
        k += 1
        s1.release()
        s2.release()
    sys.exit(0)

s1 = mp.Semaphore(1)
s2 = mp.Semaphore(1)
s3 = mp.Semaphore(0)
p1 = mp.Process(target=F1, args=(s1,s3,))
p2 = mp.Process(target=F1, args=(s2,s3,))
p3 = mp.Process(target=F1, args=(s1, s2, s3,))