"""
Filename: exercice3.py
Author: Adélie Gibou
Date: 05 may 2025
Description: 
"""

import os,sys
N = 10
v=1
while os.fork()==0 and v<=N :
    v += 1
print(v)
sys.exit(0)