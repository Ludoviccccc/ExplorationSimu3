import sys
sys.path.append('../../')
import pickle
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
from exploration.history import History
from visualisation.visu import plot_ddr_miss_ratio_diversity,hist_diversity_misses
from visualisation.visu_plotly import plot_time_diversity_plotly
from exploration.load_file import load
from visualisation.visu_total_div import plot_total_diversity
import os
import json
if __name__=='__main__':
    with open(sys.argv[1],"rb") as f:
        config = json.load(f)
    N = config['N']
    k_list = config['k_values']
    s_list = config['s_values']
    folder = 'results' 
    os.system('mkdir images')
    images = 'images'
    excl = 'imgep raw data'

    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
    for k in k_list:
        for s in s_list:  
            name = f'{folder}/imgep_run_{k}_{N}_s_{s}'
            content_imgep = load(name)
            plot_time_diversity_plotly(content_rand,content_imgep, f'{images}/time_k_{k}_s_{s}_plotly', show=False,title=f'diversity for time {excl} k={k},s={s}')


    plot_total_diversity(content_rand,[(load(f'{folder}/imgep_run_{k}_{N}_s_{s}'),f'imgep k = {k},seg={s}') for k in k_list for s in s_list],name=f'{images}/diversity_comparaison')


    hist_diversity_misses(content_rand['memory_perf'],
        [load(f'{folder}/imgep_run_{k}_{N}_s_{s}')['memory_perf'] for k in k_list for s in s_list ],
        name=f"{images}/misses",
        num_row=3,
        title=f"Diveristy ddr miss ratio mutual vs isolation with N={N} iterations. b:bank, r:row",
        labels=[f'seg={s},k={k}' for k in k_list for s in s_list]
    )

