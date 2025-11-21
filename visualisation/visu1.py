import matplotlib.pyplot as plt
import numpy as np
import time
import os

def cumulated_squared_distance_to_cloud(tab):
    '''
    returns sum of pair wise squared distances
    '''
    max_ = np.max(tab,axis=0)
    factors = np.ones(tab.shape[1])
    factors[np.where(max_<=1.0)[0]] = 200
    factors /=np.sum(factors)
    diff = lambda j: np.sum((factors*(tab[j+1:,:]-tab[j,:]))**2)
    diff_ = np.vectorize(diff)
    start = time.time()
    sum_ = np.sum(diff_(np.arange(len(tab))))
    print(time.time()-start)
    return sum_
def bin_diversity(content):
    div = 20*np.ones(content.shape[1])
    coords = (content)//div
    c = np.unique(coords,axis=0)
    return c
def diversity_for_comparaison_bin_method(args:list[np.ndarray],name=None,title=None):
    labels = []
    contents = []
    diversities = []
    plt.figure()
    step = 500
    for value in args:
        content = value[0]
        label = value[1]
        labels.append(label)
        diversity = [0] + [len(bin_diversity(content['tabular_view'][:j])) for j in range(100,len(content['tabular_view']),step)]+ [len(bin_diversity(content['tabular_view']))]
        plt.plot(range(0,len(content['tabular_view'])+step+1,step),diversity,'-o',label=label)
    plt.grid()
    plt.ylabel('diversity:bins filled ',fontsize=19)
    plt.xlabel('iteration',fontsize=19)
    plt.legend( prop={'size': 19})
    if title:
        plt.title(title,fontsize=19)
    if name:
        k = 0
        while os.path.isfile(f'{name}_{k}.png'):
            k+=1
        plt.savefig(f'{name}_{k}.png')
    plt.show()
    return labels,diversities
def polytope_to_cloud(tab):
    '''
    returns sum of pair wise squared distances
    '''
    max_ = np.max(tab,axis=0)
    #factors = np.array([1.0/400 if max_[j]>1.0 else 1.0 for j in range(tab.shape[1])]).reshape((1,-1))
    #idx = np.array([j for j in range(tab.shape[1]) if max_[j]<=1.0])
    idx = np.where(max_<=1.0)[0]
    diff = lambda j: np.max(np.abs(tab[j+1:,idx]-tab[j,idx]))#(N-j,dim)
    diff_ = np.vectorize(diff)
    start = time.time()
    sum_ = np.max(diff_(np.arange(len(tab)-2)))
    print(time.time()-start)
    return sum_

def histogram_diversity_for_comparaison(args:list[np.ndarray],name=None,title=None):
    labels = []
    contents = []
    diversities = []
    plt.figure(figsize=(20,10))
    for value in args:
        content = value[0]
        label = value[1]
        labels.append(label)
        diversity_ = cumulated_squared_distance_to_cloud(content['tabular_view']) 
        #diversity_ = polytope_to_cloud(content['tabular_view']) 
        plt.bar([label],[diversity_])
        diversities.append(diversity_)
        contents.append(content)
    if title:
        plt.title(title)
    if name:
        k = 0
        while os.path.isfile(f'{name}_{k}.png'):
            k+=1
        plt.savefig(f'{name}_{k}.png')
    plt.show()
    return labels,diversities
def comparaison(args:list[np.ndarray],name):
    plt.figure()
    for value in args:
        content = value[0]
        label = value[1]
        x = content['memory_perf']['mutual']['time_core0']
        y = content['memory_perf']['mutual']['miss_ratios_global']
        plt.scatter(x,y[:,0],label=label)
    plt.xlabel('time core0')
    plt.ylabel('miss ratio bank0')
    plt.legend()
    if name:
        plt.savefig(name)
    plt.show()
def maxtrix_squared_distance_to_cloud(tab):
    '''
    returns sum of pair wise squared distances
    '''
    max_ = np.max(tab,axis=0)
    factors = np.array([1.0/400 if max_[j]>1.0 else 1.0 for j in range(tab.shape[1])]).reshape((1,-1))
    factors = factors/np.sum(factors)
    idx = np.array([j for j in range(tab.shape[1]) if max_[j]<=1.0])
    diff = lambda j: ((tab[j+1:,idx]-tab[j,idx]))**2
    diff_ = np.vectorize(diff)
    start = time.time()
    sum_ = diff_(np.arange(len(tab)))
    return sum_
