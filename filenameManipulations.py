# filenameManipulations.py
# Author: Tynan Kennedy
# Date: July 29, 2020

# Just some basic functions to import elsewhere

import numpy as np

def swapExtension(filename, newExtension):
    i = len(filename)
    for a in range(i):
        if filename[i-1-a] == '.':
            baseName = filename[0:i-a]
            break
    newFilename = baseName + newExtension
    return newFilename

def swapPrefix(filename, newPrefix):
    i = len(filename)
    for a in range(i):
        if filename[a] == '_':
            baseName = filename[a+1:]
            break
    newFilename = newPrefix + baseName
    return newFilename

def stripExtension(filename):
    i = len(filename)
    for a in range(i):
        if filename[i-1-a] == '.':
            baseName = filename[0:i-1-a]
            break
    return baseName

def addPrefix(filename, prefix):
    return prefix + filename

def extractPrefix(filename):
    i = len(filename)
    for a in range(i):
        if filename[a] == '_':
            prefix = filename[0:a]
            break
    return prefix

def stripPrefix(filename):
    return swapPrefix(filename, '')