import pickle
import numpy as np
import os

def load(name,k=None):
    if k==None:
        k = 1
        while os.path.isfile(f"{name}_{k}.pkl"):
            k+=1
        k-=1
    with open(f'{name}_{k}.pkl','rb') as f:
        contentbis = pickle.load(f)
    print(f'{name}_{k}.pkl')

    return contentbis

