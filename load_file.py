import pickle
import numpy as np
import os




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
    folder = 'non_exclusive_axis_exploration3' 
    folder = 'imgep_pca_results'
    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
