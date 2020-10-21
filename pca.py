#!/usr/bin/env python
# coding: utf-8

# In[1]:


from scipy.linalg import eigh  
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def load_and_center_dataset(filename):
    x = np.load(filename) 
    x = np.reshape(x,(2000,784))
    x_ = x - np.mean(x,axis=0)
    return x_


# In[3]:


def get_covariance(dataset):
    total = 0
    for i in range(len(dataset)):
        x = dataset[i].reshape(len(dataset[i]),1)
        total += np.dot(x, np.transpose(x))
    return total/(len(dataset) - 1)


# In[4]:


def get_eig(S, m):
    a,b = eigh(S)
    sorted_indices = np.argsort(abs(a))
    topk_evecs = b[:,sorted_indices[:-m-1:-1]]
    topk_values = a[sorted_indices[:-m-1:-1]]
    return np.diag(topk_values), topk_evecs


# In[5]:


def get_eig_perc(S, perc):
    a,b = eigh(S)
    sorted_indices = np.argsort(abs(a))
    values = abs(a[sorted_indices[::-1]])
    vectors = b[:,sorted_indices[::-1]]
    idx = 0 
    value_sum = np.sum(values)
    for i in range(len(values)):
        if values[i]/value_sum > perc:
            idx = i
        else:
            break
    values = values[:idx+1]
    vectors = vectors[:,:idx+1]
    return np.diag(values), vectors


# In[6]:


def project_image(image, U):
    total = 0
    for i in range(len(U[0])):
        total += np.dot(np.dot(np.transpose(U[:,i]),image),U[:,i])
    return total.reshape(len(image),1)


# In[7]:


def display_image(orig, proj):
    proj = proj.reshape(28,28)
    orig = orig.reshape(28,28)
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
    original = ax1.imshow(orig, cmap='gray', aspect='equal')
    projection = ax2.imshow(proj, cmap='gray', aspect='equal')
    ax1.set_title('Original')
    ax2.set_title('Projection')
    f.colorbar(original,ax=ax1)
    f.colorbar(projection,ax=ax2)
    plt.show( block=None)

