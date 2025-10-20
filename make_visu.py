from simulator.sim3 import *
import pickle
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
from codegeneration import generate_instruction_sequence
from simulator.sim3 import print_contention_analysis
import pandas as pd
from exploration.history import History

from visu import plot_ddr_miss_ratio_diversity, plot_time_diversity, comparaison_ratios_iterations,diversity_time_iteration,hist_diversity
import os






def load(name):
    k = 1
    while os.path.isfile(f"{name}_{k}.pkl"):
        k+=1
    k-=1
    with open(f'{name}_{k}.pkl','rb') as f:
        contentbis = pickle.load(f)
    return contentbis

if __name__=='__main__':

    N = 10000
    
    name = f'data_explor/rand_run_{N}'
    content_rand = load(name)
    
    
    for k in [2]:
        for s in [1]:  
            name = f'data_explor/imgep_run_{k}_{N}_s_{s}'
            content_imgep = load(name)
            #plot_ddr_miss_ratio_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], name=f'images/miss_ratios_k_{k}_s_{s}', show=False)
            hist_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], name=f'images/time_k_{k}_s_{s}',num_row=7)
            #comparaison_ratios_iterations([('random',content_rand['memory_perf']),('imgep',content_imgep['memory_perf'])],name='r')
            #diversity_time_iteration(content_rand['memory_perf'],content_imgep['memory_perf'],title='iteration_time')
