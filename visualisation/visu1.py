import matplotlib.pyplot as plt
import numpy as np
import time

def cumulated_squared_distance_to_cloud(tab):
    '''
    returns sum of pair wise squared distances
    '''
    max_ = np.max(tab,axis=0)
    factors = np.array([1.0/400 if max_[j]>1.0 else 1.0 for j in range(tab.shape[1])]).reshape((1,-1))
    factors = factors/np.sum(factors)
    idx = np.array([j for j in range(tab.shape[1]) if max_[j]<=1.0])
    diff = lambda j: np.sum(((tab[j+1:,idx]-tab[j,idx]))**2)
    diff_ = np.vectorize(diff)
    start = time.time()
    sum_ = np.sum(diff_(np.arange(len(tab))))
    print(time.time()-start)
    return sum_
def polytope_to_cloud(tab):
    '''
    returns sum of pair wise squared distances
    '''
    max_ = np.max(tab,axis=0)
    #factors = np.array([1.0/400 if max_[j]>1.0 else 1.0 for j in range(tab.shape[1])]).reshape((1,-1))
    idx = np.array([j for j in range(tab.shape[1]) if max_[j]<=1.0])
    diff = lambda j: np.max(np.abs(tab[j+1:,idx]-tab[j,idx]),axis=1)#(N-j,dim)
    diff_ = np.vectorize(diff)
    #[diff(ta
    start = time.time()
    sum_ = np.max(diff_(np.arange(len(tab)-2)))
    print(time.time()-start)
    return sum_

def histogram_diversity_for_comparaison(args:list[np.ndarray],name=None):
    labels = []
    contents = []
    diversities = []
    plt.figure()
    for value in args:
        content = value[0]
        label = value[1]
        labels.append(label)
        diversity_ = cumulated_squared_distance_to_cloud(content['tabular_view']) 
        #diversity_ = polytope_to_cloud(content['tabular_view']) 
        plt.bar([label],[diversity_])
        diversities.append(diversity_)
        contents.append(content)
    if name:
        plt.savefig(name)
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
