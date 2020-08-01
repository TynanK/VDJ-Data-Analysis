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

def makeArray3D(ListofListsofLists):
    len0 = len(ListOfLists)
    len1 = 0
    len2 = 0
    for a in range(len0):
        if len(ListofLists[a]) > len1:
            len1 = len(ListofLists[a])
        for b in range(len(ListofLists[a])):
            if len(ListsofListsofLists[a][b]) > len2:
                len2 = len(ListsofListsofLists[a][b])
    data = np.zeros((len0,len1,len2)) - 10
    for a in range(len0):
        for b in range(len(ListofListsofLists[a])):
            for c in range(len(ListsofListsofLists[a][b])):
                data[a,b,c] = ListofListsofLists[a][b][c]
    return data

def makeListofListsofLists(array):
    (i,j,k) = array.shape

    data = []
    for a in range(i):
        data.append([])
        for b in range(j):
            data[a].append([])
            for c in range(k):
                if array[a,b,c] != -10:
                    data[a][b].append(array[a,b,c])
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

def dataInsert3D(data_list, alpha_key_list, beta_key_listoflists, datum, alpha_key, beta_key):
    if data_list == [] and alpha_key_list == [] and beta_key_listoflists == []:
        return [[[datum]]], [alpha_key], [[beta_key]]
    else:
        if alpha_key in alpha_key_list:
            alpha_ind = alpha_key_list.index(alpha_key)
            if beta_key in beta_key_listoflists[alpha_ind]:
                beta_ind = beta_key_listoflists[alpha_ind].index(beta_key)
                data_list[alph_ind][beta_ind].append(datum)
            else:
                beta_key_listoflists[alpha_ind].append(beta_key)
                data_list[alpha_ind].append([datum])
        else:
            alpha_key_list.append(alpha_key)
            beta_key_listoflists.append([beta_key])
            data_list.append([[datum]])
    return data_list, alpha_key_list, beta_key_listoflists

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

def mergeLists3D(data1, alpha_key_list1, beta_key_listoflists1, data2, alpha_key_list2, beta_key_listoflists2):
    data3 = data1
    alpha_key_list3 = alpha_key_list1
    beta_key_listoflists3 = beta_key_listoflists1

    len0 = len(alpha_key_list2)

    for a in range(len0):
        len1 = len(beta_key_listoflists2[a])
        for b in range(len1):
            for c in range(len(data2[a][b])):
                data3, alpha_key_list_3, beta_key_listoflists3 = dataInsert3D(data3, alpha_key_list3, beta_key_listoflists3, data2[a][b][c], alpha_key_list2[a], beta_key_listoflists2[a][b])

    alpha_key_list3_sorted = alpha_key_list3
    alpha_key_list3_sorted.sort()
    if alpha_key_list3_sorted != alpha_key_list3:
        data3 = [x for _,x in sorted(zip(data3, alpha_key_list3))]
        beta_key_listoflists3 = [x for _,x in sorted(zip(beta_key_listoflists3, alpha_key_list3))]
        alpha_key_list3 = alpha_key_list3_sorted
    
    len0 = len(alpha_key_list3)
    for a in range(len0):
        beta_key_list3_sorted = beta_key_list3[a]
        beta_key_list3_sorted.sort()
        if beta_key_list3_sorted != beta_key_list3[a]:
            data3[a] = [x for _,x in sorted(zip(data3[a], beta_key_list3[a]))]
            beta_key_list3[a] = beta_key_list3_sorted
    
    return data3, alpha_key_list3, beta_key_listoflists3