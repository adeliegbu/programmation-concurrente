"""
Filename: exercice7.py
Author: Adélie Gibou
Date: 12 may 2025
Description: 
"""

import os,sys

N = 3
for i in range(N) :
#__________début des ajouts_________
    os.fork()
    os.fork()
# __________fin des ajouts__________
print("Bonjour")
sys.exit(0) 