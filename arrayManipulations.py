# arrayManipulations.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# Just some helper functions
import numpy as np

def makeArray(ListOfLists):
    len0 = len(ListOfLists)
    len1 = 0
    for a in range(len0):
        if len(ListOfLists[a]) > len1:
            len1 = len(ListOfLists[a])
    data = np.zeros((len0,len1)) - 10
    for a in range(len0):
        for b in range(len(ListOfLists[a])):
            data[a,b] = ListOfLists[a][b]
    return data

def makeListOfLists(array):
    (i,j) = array.shape

    data = []
    for a in range(i):
        data.append([])
        for b in range(j):
            if array[a,b] != -10:
                data[a].append(array[a,b])
    return data

def dataInsert(data_list, key_list, datum, key):
    if key_list == [] and data_list == []:
        return [[datum]], [key]
    else:
        if key in key_list:
            key_ind = key_list.index(key)
            data_list[key_ind].append(datum)
        else:
            key_list.append(key)
            data_list.append([datum])
        return data_list, key_list

def mergeLists(data1, key1, data2, key2):
    data3 = data1
    key3 = key1

    len0 = len(key2)

    for a in range(len0):
        for b in range(len(data2[a])):
            data3, key3 = dataInsert(data3, key3, data2[a][b], key2[a])
    
    key3_sorted = key3
    key3_sorted.sort()
    if key3_sorted != key3:
        data3 = [x for _,x in sorted(zip(data3, key3))]
        key3 = key3_sorted

    return data3, key3