import numpy as np
import matplotlib.pyplot as plt

def bin_diversity_time_space(content):
    '''
    bin diversity in product time space
    '''
    sup = np.where(content.max(axis=0)>1.0)[0]
    time_space = content[:,sup]
    div = 10*np.ones(time_space.shape[1])
    coords = (time_space)//div
    c = np.unique(coords,axis=0)
    return len(c)
def bin_diversity_miss_space(content):
    '''
    bin diversity in product time space
    '''
    sup = np.where(content.max(axis=0)<=1.0)[0]
    miss_space = content[:,sup]
    div = 5*np.ones(miss_space.shape[1])
    coords = 200*(miss_space)//div
    c = np.unique(coords,axis=0)
    return len(c)
def diversity_time_iteration(list_,name,title=None, folder="images"):
    plt.figure(figsize=(15,10))
    for arg in list_:
        content,label = arg[0],arg[1]
        print(content.keys())
        ll = len(content['tabular_view'])
        diversity_values = [bin_diversity_time_space(content['tabular_view'][:k]) for k in range(100,ll,100)]
        plt.plot(range(100,ll,100),diversity_values, '-o',label=label)
        plt.xlabel("iteration",fontsize=19)
        plt.ylabel("diversity",fontsize=19)
    if title:
        plt.title(title,fontsize=19)
    else:
        plt.title("time",fontsize=19)
    plt.legend(prop={'size': 19})
    if title:
        plt.savefig(f"{folder}/{name}")
    plt.show()
    plt.close()
def diversity_miss_iteration(list_,name,title=None, folder="images"):
    plt.figure(figsize=(15,10))
    for arg in list_:
        content,label = arg[0],arg[1]
        print(content.keys())
        ll = len(content['tabular_view'])
        diversity_values = [bin_diversity_miss_space(content['tabular_view'][:k]) for k in range(100,ll,100)]
        plt.plot(range(100,ll,100),diversity_values, '-o',label=label)
        plt.xlabel("iteration",fontsize=19)
        plt.ylabel("diversity",fontsize=19)
    if title:
        plt.title(title,fontsize=19)
    else:
        plt.title("time",fontsize=19)
    plt.legend(prop={'size': 19})
    if title:
        plt.savefig(f"{folder}/{name}")
    plt.show()
    plt.close()
