"""
Filename: exercice5.py
Author: Adélie Gibou
Date: 05 may 2025
Description: 
"""
import os, sys


for n in range(2):
    if not os.fork():
    # pid = os.fork()
    # if pid == 0 :
        for i in range (100):
            print(n*100 + i + 1)
        sys.exit()
    os.wait()