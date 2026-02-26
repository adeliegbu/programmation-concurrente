"""
Filename: exercice7.py
Author: Adélie Gibou
Date: 05 may 2025
Description: 
"""

import os, sys
if (os.fork() != 0) :
    if (os.fork() == 0) :
        os.fork()
        print("1")
    else :
        print("2")
else :
    print("3")
print("4")
sys.exit(0)
