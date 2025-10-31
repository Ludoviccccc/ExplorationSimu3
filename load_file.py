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
from visualisation.visu1 import histogram_diversity_for_comparaison, comparaison




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

    N = 10000
    folder = 'non_exclusive_axis_exploration2' 
    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
