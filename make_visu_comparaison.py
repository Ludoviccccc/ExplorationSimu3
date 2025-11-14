from simulator.sim3 import *
import pickle
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
from simulator.sim3 import print_contention_analysis
import pandas as pd
from exploration.history import History

from visualisation.visu import plot_ddr_miss_ratio_diversity, plot_time_diversity, comparaison_ratios_iterations,hist_diversity_misses,diversity_time_iteration2
import os
from visualisation.visu_plotly import plot_time_diversity_plotly
from visualisation.visu1 import histogram_diversity_for_comparaison, comparaison, histogram_diversity_for_comparaison_bin_method,diversity_for_comparaison_bin_method
from visualisation.visu_time import diversity_time_iteration,diversity_miss_iteration




def load(name):
    k = 1
    while os.path.isfile(f"{name}_{k}.pkl"):
        k+=1
    k-=1
    with open(f'{name}_{k}.pkl','rb') as f:
        contentbis = pickle.load(f)
    print(f'{name}_{k}.pkl')
    return contentbis

if __name__=='__main__':

    N = 100000
    folder = 'non_exclusive_axis_exploration' 
    images = 'images_non_excl'
    excl = 'imgep raw data'

    #folder = 'imgep_pca_results' 
    #images = 'images_pca'
    #excl = 'imgep pca'

    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
    s_list = [1]

    for k in [1]:
        for s in s_list:  
            name = f'{folder}/imgep_run_{k}_{N}_s_{s}'
            content_imgep = load(name)
            plot_time_diversity_plotly(content_rand,content_imgep, f'{images}/time_k_{k}_s_{s}_plotly', show=False,title=f'diversity for time {excl} k={k}')

    exit()
    diversity_time_iteration([(content_rand,'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}'),f'imgep k = {k},segment = {s}') for k in [1,] for s in s_list], name=f'iteration_time_',title=f'diversity time space, {excl}',folder=images)

    #histogram_diversity_for_comparaison([(content_rand,'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}'),f'imgep k = {k},seg={s}') for k in [1,2,3] for s in s_list],f'{images}/comparaison_models',title=f'diversity {excl}')

    hist_diversity_misses(content_rand['memory_perf'],
        [load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf'] for k in [1] for s in s_list for folder in ['non_exclusive_axis_exploration']],
        name=f"misses",
        num_row=7,
        title=f"diveristy ddr miss ratio mutual vs isolation with N={N} iterations",
        labels=[f'seg={s},k={k}' for k in range(1,4) for s in s_list]
    )

    '''
    to see if there is correlation between time execution and miss ratio
    '''
    #comparaison([(content_rand,'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}'),f'imgep k = {k},segment = {s}') for k in [1,2,3] for s in [1]],f'{images}/all_space_diversity_comparaison')



    #arg_list = [('random',content_rand['memory_perf'])]+[(f'imgep k = {k},segment = {s}',load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf']) for k in [1,2,3] for s in [0]]

    #comparaison_ratios_iterations(arg_list,name=f'{images}/comparaison_iteration_ddr_miss_ratio',num_rows=7)

    #diversity_miss_iteration([(content_rand,'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}'),f'imgep k = {k},segment = {s}') for k in [1,2,3] for s in [1]], name=f'iteration_miss_',title='diversity miss space',folder=images)
