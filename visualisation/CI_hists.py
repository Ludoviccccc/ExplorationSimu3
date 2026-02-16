import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import pickle
import os
import sys
sys.path.append('../')
from exploration.load_file import open_content_all_list
from scipy.special import stdtr,stdtrit
import pandas as pd

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
    return {'mean':mean_,'inf':inf,'sup':sup}

def diversity(data:[np.ndarray,np.ndarray],bins:[np.ndarray, np.ndarray]):
    H,_,_ = np.histogram2d(data[0],data[1],bins)
    divers = np.sum(H>0)
    return divers
def hist_diversity_misses(content:list,
                          num_bank=4,
                          num_row = 2,
                          ):
    Diversity_DDR_core0 = []
    Diversity_DDR_core1 = []
    #labels = []
    bins = np.arange(-1.0,1.0,0.05)
    for j in range(num_bank):
        for row in range(num_row):
            diversity_ratio0 = diversity([content['mutual']['miss_ratios_detailled'][:,row,j],
                            content['core0']['miss_ratios_detailled'][:,row,j]], [bins, bins])
            diversity_ratio1 = diversity([content['mutual']['miss_ratios_detailled'][:,row,j],
                            content['core1']['miss_ratios_detailled'][:,row,j]], [bins, bins])
            Diversity_DDR_core0.append(diversity_ratio0)
            Diversity_DDR_core1.append(diversity_ratio1)
            #labels.append(f'b{j},r{row}')
    return Diversity_DDR_core0,Diversity_DDR_core1

if __name__=='__main__':
    N = 10000
    k_values = [1,2,3]
    folder = '../results_20'
    algo_list = ['imgep','operators','rand']
    CI_diversity_algo_core0 = pd.DataFrame([])
    CI_diversity_algo_core1 = pd.DataFrame([])
    M = 500
    n_func = 3
    j_list = range(M)
    for algo in algo_list:
        for k in k_values:
            if algo=='rand' and k>1:
                break
            print('opening data',algo,f'k={k}')
            n_p = 5
            n_func = 20
            content_list = []
            for l in range(1+M//(n_func*n_p)):
                if l ==M//(n_func*n_p):
                    with Pool(70) as p: 
                        content_list_temp = [open_content_all_list(folder,k,N,algo)(range(l,l+M%(n_p*n_func)))]
                else:
                    with Pool(70) as p: 
                        content_list_temp = p.map(open_content_all_list(folder,k,N,algo),[range(n_func*n_p*l+m*n_p,n_func*n_p*l+(m+1)*n_p) for m in range(n_func)])
                for element in content_list_temp:
                    content_list +=element
            if len(content_list)==0:
                raise ValueError('empty content list')
            else:
                print(f"{len(content_list)} elements in content list")
            diversity_list = []
            print('computing diversity in parallel')
            n_func = 20
            for j in range(1+len(content_list)//n_func):
                if j==len(content_list)//n_func:
                    with Pool(70) as p:
                        batch_div = p.map(hist_diversity_misses,content_list[j*n_func:])
                else:
                    with Pool(70) as p:
                        batch_div = p.map(hist_diversity_misses,content_list[j*n_func:(j+1)*n_func])
                diversity_list+=batch_div
            print('diversity computeted',algo,f'k={k}')
            diversity_list = np.array(diversity_list)
            diversity_0 = diversity_list[:,0,:]
            diversity_1 = diversity_list[:,1,:]
            CI_diversity_algo_core0[f'{algo}_{k}'] = CI(diversity_0)
            CI_diversity_algo_core1[f'{algo}_{k}'] = CI(diversity_1)

    name0  = 'ci_histogram_diveristy_core0.csv'
    CI_diversity_algo_core0.to_csv(name0)
    print(f'{name0} written!')
    name1  = 'ci_histogram_diveristy_core1.csv'
    CI_diversity_algo_core1.to_csv(name1)
    print(f'{name1} written!')
