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
from exploration.load_file import load


if __name__=='__main__':

    N = 10000
    folder = 'non_exclusive_axis_exploration' 
    images = 'images_non_excl'
    excl = 'imgep raw data'

    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
    s_list = [0]
    k_list = [2]
#    for k in k_list:
#        for s in s_list:  
#            name = f'{folder}/imgep_run_{k}_{N}_s_{s}'
#            content_imgep = load(name)
#            plot_time_diversity_plotly(content_rand,content_imgep, f'{images}/time_k_{k}_s_{s}_plotly', show=False,title=f'diversity for time {excl} k={k},s={s}')
#
    #diversity_time_iteration([(content_rand,'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}'),f'imgep k = {k},segment = {s}') for k in [1,10,20] for s in s_list], name=f'iteration_time_',title=f'diversity time space, {excl}',folder=images)

    histogram_diversity_for_comparaison([(content_rand,'random')]+[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}'),f'imgep k = {k},seg={s}') for k in [2] for s in s_list],f'{images}/comparaison_models',title=f'diversity {excl}')

#    hist_diversity_misses(content_rand['memory_perf'],
#        [load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf'] for k in [2] for s in s_list for folder in ['non_exclusive_axis_exploration']],
#        name=f"misses",
#        num_row=4,
#        title=f"diveristy ddr miss ratio mutual vs isolation with N={N} iterations",
#        labels=[f'seg={s},k={k}' for k in k_list for s in s_list]
#    )
#
