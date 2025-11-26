import sys
sys.path.append('../../')
import pickle
import numpy as np
from exploration.load_file import load
import os
import json
from visualisation.visu_test import compute_total_diversity
if __name__=='__main__':
    with open(sys.argv[1],"rb") as f:
        config = json.load(f)
    N = config['N']
    k_list = config['k_values']
    folder = 'results' 
    os.system('mkdir images')
    images = 'images'
    excl = 'imgep raw data'

    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
    compute_total_diversity(content_rand,[(load(f'{folder}/imgep_run_{k}_{N}'),f'imgep k = {k}') for k in     k_list],m=20,name='diversity_comparaison')
