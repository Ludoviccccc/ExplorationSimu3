import numpy as np
import sys
sys.path.append('../../')
#from exploration.imgep.ball_areas import BallCloud1D
#from 

from simulator.sim3 import *
import pickle
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
from codegeneration import generate_instruction_sequence
from simulator.sim3 import print_contention_analysis
from exploration.history import History

class ALP_module:
    '''
    use areas to calculate reward
    '''
    def __init__(self,H:History):
        self.H = H
        self.modules_diversity = self._compute_diversty_init()
        self.modules_histograms = []
    def diversity(self,tab,bins):
        A,_ = np.histogram(tab,bins)
        self.modules
        return A
    def _compute_diversty_init(self):
        modules_diversity = []
        array = self.H.as_array()
        for j in range(array.shape[1]):
            if j<4:
                A,_ = np.histogram(array[:,j],range(0,300,5))
                self.modules_histograms.append(A)
                self.modules_diversity(sum(A>0))
            else:
                A,_ = np.histogram(array[:,j],np.linspace(0,1,21))
                self.modules_histograms.append(A)
                self.modules_diversity(sum(A>0))
        return modules_diversity
    def update_diversity(self):
        tab = self.H.as_tab()
        v2bin = lambda v,step: ((v//step)*step,(v//step)*step + step)
        v2id = lambda v,step: (v//step)
        v2id2 = lambda v,step: (round(v,2)*100)//step
        for j in range(tab.shape[1]):
            if max(tab[:,j])>1:
                value = tab[:,-1]
            else:
                value = round(v,2)*100
            id_ = v2id(tab[:,-1],step=5)#what histogram bin for the last added value
            self.modules_histograms[j][id_]+=1
            self.modules_diversity[j] = sum(self.modules_histograms[j]>0)
            


from visualisation.visu import plot_ddr_miss_ratio_diversity, plot_time_diversity
import os
def load(name):
    k = 1
    while os.path.isfile(f"{name}_{k}.pkl"):
        k+=1
    k-=1
    with open(f'{name}_{k}.pkl','rb') as f:
        contentbis = pickle.load(f)
    return contentbis

E =Env(300,num_addr=100)
H_rand = History(env = E)
N = 10000
name = f'data_explor/rand_run_{N}'
content_rand = load(name)

#step = 5
#counts = np.zeros(300//step)
#bins = range(0,300,step)
#t2bin = lambda t,step: ((t//step)*step,(t//step)*step +5)
#t2id = lambda t,step: (t//step)
#for t in times:
#    id_ = t2id(t=t,step=step)
#    counts[id_] +=1
H_rand.take(content_rand,10000)
#array = H_rand.as_array()
#
#modules_diversity  =[]
#for j in range(array.shape[1]):
#    if j<4:
#        modules_diversity.append(diversity(array[:,j],range(0,300,5)))
#    else:
#        modules_diversity.append(diversity(array[:,j],np.linspace(0,1,21)))
#print(array)
#print(modules_diversity)
alp = ALP_module(H_rand)
print(alp.modules_diversity)
