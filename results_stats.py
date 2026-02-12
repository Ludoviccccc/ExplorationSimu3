import sys
sys.path.append('../../')
import pickle
import os
import numpy as np
from scipy.special import stdtr, stdtrit
from multiprocessing import Pool
# This codes evaluates the diversity evolution of multiple IMGEP/RANDOM exploration runs
# in parallel (using Pool) and determines asymptotic confidence intervals for each point of the curves

def bin_diversity(content):
    div = 5*np.ones(content.shape[1])
    coords = (content)//div
    c = np.unique(coords,axis=0)
    return c

def evaluate_hist_diversity(content_list):
    step = 1000
    n_func = 5
    diversity = [0]+ [len(bin_diversity(content_list[:j])) for j in range(0,len(content_list),step) if j!=0]+ [len(bin_diversity(content_list))]
    return diversity
def Sn(diversity_array:np.ndarray):
    """
    computes the sigma estimator of the diversity values
    """
    mean_ = diversity_array.mean(axis=0)
    out = np.sqrt(np.sum((diversity_array - mean_)**2,axis=0)/(diversity_array.shape[0]-1))
    return out
def CI(diversity_array,alpha=.05):
    n = diversity_array.shape[0]
    qt = stdtrit(n-1,1-alpha)
    sig = Sn(diversity_array)
    mean_ = diversity_array.mean(axis=0)
    inf = mean_ - qt*sig*(1.0/np.sqrt(n))
    sup = mean_ + qt*sig*(1.0/np.sqrt(n))
    x_axis = 1000*np.arange(len(mean_))
    return {'mean':mean_,'inf':inf,'sup':sup,'iterations':x_axis}

if __name__=='__main__':
    N = 10000
    k_values = [1,2,3]
    folder = 'results' 
    algo_list = ['imgep','operators','rand']
    CI_algo = {algo:{k:[] for k in k_values} for algo in algo_list}
    N = 10000
    M = 20
    j_list = range(M)
    print('start opening files')
    for algo in algo_list:
        for k in k_values:
            content_list = []
            for j in j_list:
                if algo in ['imgep','operators']:
                    name = f'{algo}_run_{k}_{N}_{j}.pkl'
                else:
                    if k>1:
                        break
                    name = f'{algo}_run_{N}_{j}.pkl'
                if j%100==0:
                    print(f'opening {name}')
                try:
                    with open(os.path.join(folder,name),'rb') as f:
                        stats = pickle.load(f)
                        content_list.append(stats['tabular_view'])
                except:
                    print(f'fail at opening {name}')
            content_list = content_list
            diversity_list = []
            n_func = 10
            for j in range(len(content_list)//n_func):
                with Pool(40) as p: 
                    batch_div = p.map(evaluate_hist_diversity,content_list[j*n_func:(j+1)*n_func])
                diversity_list+=batch_div
            diversity_list = np.array(diversity_list)
            print('diversity_list', diversity_list.shape,algo,f'k={k}')
            CI_algo[algo][k] = CI(diversity_list)
    with open('ci_diversity.pkl','wb') as f:
        pickle.dump(CI_algo,f)
    print('dumped!')
