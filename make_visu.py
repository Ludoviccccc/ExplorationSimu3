from simulator.sim3 import *
import pickle
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
import pandas as pd
from exploration.history import History

from visualisation.visu import plot_ddr_miss_ratio_diversity, plot_time_diversity, comparaison_ratios_iterations,diversity_time_iteration,hist_diversity_misses,diversity_time_iteration2
import os
from visualisation.visu_plotly import plot_time_diversity_plotly




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
    folder = 'non_exclusive_axis_exploration' 
    images = 'images_non_excl'
    method = 'imgep raw matrix'
    s_list = [0]
    k_list = [1,2,5,10,20]

    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)

    diversity_time_iteration2([(content_rand['memory_perf'],'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf'],f'imgep k = {k},segment = {s}') for k in k_list for s in s_list], title=f'iteration_time_',folder=images)
    #arg_list = [('random',content_rand['memory_perf'])]+[(f'imgep k = {k},segment = {s}',load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf']) for k in [1,2,3] for s in [1]]

    #comparaison_ratios_iterations(arg_list,name=f'{images}/comparaison_iteration_ddr_miss_ratio',num_rows=7)
    
    #for k in [1,2,3]:
    #    for s in [1]:  
    #        name = f'{folder}/imgep_run_{k}_{N}_s_{s}'
    #        content_imgep = load(name)
    #        plot_ddr_miss_ratio_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], name=f'{images}/miss_ratios_k_{k}_s_{s}', show=False,num_row=7)
    #        #plot_time_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], f'{images}/time_k_{k}_s_{s}', show=False)

    hist_diversity_misses(content_rand['memory_perf'],[load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf'] for k in [2,3,1] for s in s_list], name=f'{images}/misses',num_row=7,title=f'diveristy ddr miss ratio mutual vs isolation with N={N} iterations, {method}',labels=[f'seg={s},k={k}' for k in range(1,4) for s in [1]])
