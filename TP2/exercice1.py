"""
Filename: exercice1.py
Author: Adélie Gibou
Date: 12 may 2025
Description: 
"""

import os,sys
p=1
while p>0 :
    p = os.fork()
    os.execlp("python3" , "python3" , "exercice1bis.py" )
    sys.exit(0)