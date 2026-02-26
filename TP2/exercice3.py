"""
Filename: exercice3.py
Author: Adélie Gibou
Date: 12 may 2025
Description: 
"""

import os,sys

liste = [["who"],["ps"],[["ls"],["-l"]]]

for i in liste:
    pid = os.fork()
    if pid == 0 :
        os.execvp(i[0], i)
    