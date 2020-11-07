#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt


# In[2]:


def load_data(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        pokemon = []
        idx = 0
        for row in reader:
            idx += 1
            if idx <= 20:
                row.pop('Generation')
                row.pop('Legendary')
                pokemon.append(row)
    return pokemon


# In[3]:


def calculate_x_y(stats):
    x = int(stats['Attack']) + int(stats['Sp. Atk']) + int(stats['Speed'])
    y = int(stats['Defense']) + int(stats['Sp. Def']) + int(stats['HP'])
    return (x,y)


# In[4]:


def get_x_y(dataset):
    data = []
    for row in dataset:
        cor = calculate_x_y(row)
        data.append([cor[0],cor[1]])
    return np.array(data).reshape(20,2)


# In[5]:


def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


# In[6]:


def hac(dataset):
    dataset = dataset.tolist()
    dis = []
    z = []
    num = []
    idx = 0
    cluster_num = 20
    for p in dataset:
        for pp in dataset:
            dis.append(distance(p,pp))
    dis = np.array(dis).reshape(20,20)
    while cluster_num >1:
        i,j = np.where( dis==np.min(dis[np.nonzero(dis)]))
        if i[0] < 20 and j[0] < 20:
            num.append(2)
        elif i[0] < 20 and j[0] >= 20:
            num.append(1 + num[j[0] - 20])
        else:
            num.append(num[i[0] - 20] + num[j[0] - 20])
        cluster1 = i[0]
        cluster2 = j[0]
        z.append([cluster1, cluster2, dis[cluster1,cluster2], num[idx]])
        new = []
        for point in dataset:
            new.append(min(dis[dataset.index(point),cluster1] , dis[dataset.index(point),cluster2]))  
        dis = np.insert(dis, len(dataset), values=new, axis=1)
        new.append(0)
        dis = np.insert(dis, len(dataset),values=new, axis = 0 )
        dis[cluster1,:] = 0
        dis[:,cluster1] = 0
        dis[cluster2, :] = 0
        dis[:,cluster2] = 0
        cluster_num -= 1
        idx += 1
        new_cluster = []
        new_cluster.append(dataset[cluster1])
        new_cluster.append(dataset[cluster2])
        dataset.append(new_cluster)
    return z


# In[ ]:





# In[ ]:




