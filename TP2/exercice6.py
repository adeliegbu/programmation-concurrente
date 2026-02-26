"""
Filename: exercice6.py
Author: Adélie Gibou
Date: 12 may 2025
Description: 
"""

import os, time, random, sys
for i in range(4) :
    if os.fork() != 0 :
        break
random.seed()
delai = random.randint(0,4)
time.sleep(delai)
try:
    os.wait()
except :
    None
print("Mon nom est " + chr(ord('A')+i) + " j ai dormi " + str(delai) + " secondes")
sys.exit(0)