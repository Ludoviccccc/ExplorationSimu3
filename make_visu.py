from simulator.sim3 import *
import pickle
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
from codegeneration import generate_instruction_sequence
from simulator.sim3 import print_contention_analysis
import pandas as pd
from exploration.history import History

from visualisation.visu import plot_ddr_miss_ratio_diversity, plot_time_diversity, comparaison_ratios_iterations,diversity_time_iteration,hist_diversity,diversity_time_iteration2
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
    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
    images = 'images_non_excl'

    #for k in []:
    #    for s in [1]:  
    #        name = f'{folder}/imgep_run_{k}_{N}_s_{s}'
    #        content_imgep = load(name)
    #        #plot_time_diversity_plotly(content_rand,content_imgep, f'{images}/time_k_{k}_s_{s}_plotly', show=False)

    diversity_time_iteration2([(content_rand['memory_perf'],'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf'],f'imgep k = {k},segment = {s}') for k in [1,2,3] for s in [1]], title=f'iteration_time_',folder=images)
    arg_list = [('random',content_rand['memory_perf'])]+[(f'imgep k = {k},segment = {s}',load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf']) for k in [1,2,3] for s in [1]]

    comparaison_ratios_iterations(arg_list,name=f'{images}/comparaison_iteration_ddr_miss_ratio',num_rows=7)
    
    for k in [1,3]:
        for s in [1]:  
            name = f'{folder}/imgep_run_{k}_{N}_s_{s}'
            content_imgep = load(name)
            plot_ddr_miss_ratio_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], name=f'{images}/miss_ratios_k_{k}_s_{s}', show=False,num_row=7)
            plot_ddr_miss_ratio_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], name=f'{images}/miss_ratios_k_{k}_s_{s}', show=False,num_row=7)
            hist_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], name=f'{images}/time_k_{k}_s_{s}',num_row=7,title=f'diveristy ddr miss ratio for imgep k={k}. mutual vs isolation')
            plot_time_diversity(content_rand['memory_perf'],content_imgep['memory_perf'], f'{images}/time_k_{k}_s_{s}', show=False)
