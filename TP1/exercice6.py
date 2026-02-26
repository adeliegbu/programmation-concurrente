"""
Filename: exercice6.py
Author: Adélie Gibou
Date: 05 may 2025
Description: 
"""

import os, sys
os.fork()
if (os.fork()) :
    os.fork()
print("3ETI 2024")
sys.exit(0)