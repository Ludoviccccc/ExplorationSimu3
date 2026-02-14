import sys
sys.path.append('../../')
import pickle
import os
import numpy as np
from scipy.special import stdtr, stdtrit
from multiprocessing import Pool
from exploration.load_file import open_content_list
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
    diversity_time = [0]+ [len(bin_diversity(content_list[:j,idx_time])) for j in range(0,len(content_list),step) if j!=0]+ [len(bin_diversity(content_list[:,idx_time]))]
    diversity_remain = [0]+ [len(bin_diversity(content_list[:j,idx_remain])) for j in range(0,len(content_list),step) if j!=0]+ [len(bin_diversity(content_list[:,idx_remain]))]
    return [diversity_time,diversity_remain]
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
    k_values = [1]
    folder = 'results' 
    algo_list = ['imgep','operators','rand']
    CI_algo_time = {algo:{k:[] for k in k_values} for algo in algo_list}
    CI_algo_remain = {algo:{k:[] for k in k_values} for algo in algo_list}
    N = 10000
    M = 20
    time_var = ['mutual_diff_time_core0',
                 'mutual_diff_time_core1',
                 'mutual_diff_time']
    j_list = range(M)
    print('start opening files')
    for algo in algo_list:
        for k in k_values:
            if algo=='rand' and k>1:
                break
            content_list = []
            n_p = 5
            n_func = 10
            for l in range(1+M//(n_func*n_p)):
                if l ==M//(n_func*n_p):
                    with Pool(70) as p: 
                        func_open = open_content_list(folder,k,N,algo)
                        content_list_temp = [func_open(range(l,l+M%(n_p*n_func)))]
                else:
                    with Pool(70) as p: 
                        content_list_temp = p.map(open_content_list(folder,k,N,algo),[range(n_func*n_p*l+m*n_p,n_func*n_p*l+(m+1)*n_p) for m in range(n_func)])
                for element in content_list_temp:
                    content_list +=element
            idx_time = func_open.idx_time
            idx_remain = func_open.idx_remain
            if len(content_list)==0:
                raise ValueError('empty content list')

            diversity_list = []
            n_func = 10
            for j in range(len(content_list)//n_func):
                with Pool(40) as p: 
                    batch_div = p.map(evaluate_hist_diversity,content_list[j*n_func:(j+1)*n_func])
                diversity_list+=batch_div
            diversity_list = np.array(diversity_list)
            diversity_array_time = diversity_list[:,0,:]
            diversity_array_remain = diversity_list[:,1,:]
            print('diversity_array_time', diversity_array_time.shape,algo,f'k={k}')
            print('diversity_array_remain', diversity_array_remain.shape,algo,f'k={k}')
            CI_algo_time[algo][k] = CI(diversity_array_time)
            CI_algo_remain[algo][k] = CI(diversity_array_remain)
    with open('ci_diversity_time.pkl','wb') as f:
        pickle.dump(CI_algo_time,f)
    print('dumped!')
    with open('ci_diversity_remain.pkl','wb') as f:
        pickle.dump(CI_algo_remain,f)
    print('dumped!')
