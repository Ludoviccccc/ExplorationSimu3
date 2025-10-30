from simulator.sim3 import *
import pickle
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
from codegeneration import generate_instruction_sequence
from simulator.sim3 import print_contention_analysis
import pandas as pd
from exploration.history import History

from visualisation.visu import plot_ddr_miss_ratio_diversity, plot_time_diversity
import os


from exploration.imgep.OptimizationPolicy2 import OptimizationPolicykNN as OP
from exploration.imgep.goal_generator2 import GoalGenerator as G
from exploration.imgep.imgep2 import IMGEP



if __name__=="__main__":

    N = 10000
    N_init = 1000
    k_values = [1,2,3]
    num_mutations = 1
    periode = 1
    min_address_core0 = 0
    min_address_core1 = 49
    max_address_core0 = 50
    max_address_core1 = 100
    folder = 'non_exclusive_axis_exploration'
    for segment_method in [True]:
        for k in k_values:
            print('k',k)
            print('segment mixing method', segment_method)
            E =Env(400,num_addr=100)
            H = History(env=E,capacity=N)
            Pi = OP(num_mutations = num_mutations,k=k,
                    segment_method=segment_method,
                    min_address_core0=min_address_core0,
                    max_address_core0=max_address_core0,
                    min_address_core1=min_address_core1,
                    max_address_core1=max_address_core0)
            goal_generator = G()
            imgep = IMGEP(N,N_init,E,H,goal_generator,Pi, periode = periode,
                          min_address_core0=min_address_core0,
                          max_address_core0=max_address_core0,
                          min_address_core1=min_address_core1,
                          max_address_core1=max_address_core1)
            imgep()
            s = 1 if segment_method else 0
            H.save_pickle(f'{folder}/imgep_run_{k}_{N}_s_{s}')
