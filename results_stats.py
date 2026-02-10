import sys
sys.path.append('../../')
import pickle
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import stdtr, stdtrit

def bin_diversity(content):
    div = 5*np.ones(content.shape[1])
    coords = (content)//div
    c = np.unique(coords,axis=0)
    return c

def evaluate_hist_diversity(content_list):
    #hist diversity for imgep
    step = 1000
    diversity_list = []
    for f,content in enumerate(content_list):
        diversity = [0]+ [len(bin_diversity(content[:j])) for j in range(0,len(content),step) if j!=0]+ [len(bin_diversity(content))]
        diversity_list.append(diversity)
    return diversity_list
def Sn(diversity_array:np.ndarray):
    """
    computes the sigma estimator of the diversity values
    """
    out = np.sqrt(np.sum((diversity_array - diversity_array.mean(axis=0))**2,axis=0)/(diversity_array.shape[0]-1))
    return out
def CI(diversity_array,alpha=.05):
    n = diversity_array.shape[0]
    print('n',n)
    qt = stdtrit(n-1,1-alpha)
    print('qt', qt)
    sig = Sn(diversity_array)
    print('sig',sig)
    #exit()
    inf = diversity_array.mean(axis=0) - qt*sig*(1.0/np.sqrt(n))
    sup = diversity_array.mean(axis=0) + qt*sig*(1.0/np.sqrt(n))
    return inf,sup

if __name__=='__main__':
    N = 10000
    k_values = [1]
    N_init = 1000
    folder = 'results' 
    algo = ['imgep_run_1']+['operators_run_1']+['rand_run']
    N = 10000
    id_ = 2
    M = 10
    j_list = range(M)
    content_imgep_list = []
    for j in j_list:
        with open(os.path.join('results',f'{algo[id_]}_{N}_{j}.pkl'),'rb') as f:
            stats = pickle.load(f)
            content_imgep_list.append(stats['tabular_view'])
    print('len content list', len(content_imgep_list))
    print('len content', len(content_imgep_list[-1]))

    diversity_list = np.array(evaluate_hist_diversity(content_imgep_list))

    ll = np.arange(0,N+1,1000)
    print("ll",len(ll))
    for j in range(M):
        plt.plot(ll,diversity_list[j])
    plt.xlabel('iterations')
    plt.ylabel('diversity')
    plt.savefig("distinct_imgep.png")



    sn = Sn(diversity_list)
    print(sn.shape)
    print(sn)
    print(CI(diversity_list))

    #diversities_imgep_mean = stats['imgep']['mean']
    #diversities_imgep_var = stats['imgep']['var']

    #diversities_rand_mean = stats['random']['mean']
    #diversities_rand_var = stats['random']['var']
    #t_crit_interval = stats['t_crit_interval']
    #m = stats['m']
    #print(diversities_imgep_mean.shape)
    #start = 0
    #for f in range(diversities_imgep_mean.shape[0]):
    #    y = diversities_imgep_mean[f][start:]
    #    x = np.arange(0,N+1,1000)[start:]
    #    ci = diversities_imgep_var[f][start:] *t_crit_interval[1]/np.sqrt(m)
    #    print('ci shape', ci.shape)
    #    plt.plot(x,y,'-o',label=[1,2,3][f])
    #    #plt.fill_between(x, (y-ci), (y+ci), color='b', alpha=.1)
    #plt.plot(np.arange(0,N+1,1000)[start:],diversities_rand_mean[start:],'-o',label=f'random')
    #plt.grid()
    #plt.title('Entire space Diversity IMGEP vs RANDOM', fontsize=M)
    #plt.ylabel('sum of squares of distances between all pairs', fontsize=12)
    #plt.xlabel('iterations', fontsize=M)
    #plt.xticks(range(0,10001,1000)[start:])
    #plt.legend(prop={'size': M})
    #plt.show()
