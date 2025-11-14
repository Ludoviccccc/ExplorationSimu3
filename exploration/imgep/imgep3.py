import sys
sys.path.append("../")
sys.path.append("../../")
from exploration.env.func import Env
from exploration.history2 import History
from exploration.imgep.OptimizationPolicy3 import OptimizationPolicykNN
from exploration.imgep.goal_generator3 import GoalGenerator
from exploration.codegeneration import generate_instruction_sequence
import random

from exploration.codegeneration import generate_instruction_sequence
from exploration.random.func import RANDOM
import time
import numpy as np
class IMGEP:
    """
    N: int. The experimental budget
    N_init: int. Number of experiments at random
    H: History. Buffer containing codes and signature pairs
    G: GoalGenerator.
    Pi: OptimizationPolicy.
    """
    def __init__(self,
                N:int,
                N_init:int,
                E:Env,
                H:History,
                G:GoalGenerator,
                Pi:OptimizationPolicykNN,
                periode:int = 1,
                min_address_core0=0,
                max_address_core0=10,
                min_address_core1=11,
                max_address_core1=21,
                num_instructions = None,
                max_cycle:int=60,
                ):
        self.max_cycle = max_cycle
        self.N = N
        self.env = E
        self.H = H
        self.G = G
        self.N_init = N_init
        self.Pi = Pi
        self.periode = periode
        self.start = 0
        self.num_instructions = num_instructions
        self.min_address_core0 = min_address_core0
        self.max_address_core0 = max_address_core0
        self.min_address_core1 = min_address_core1
        self.max_address_core1 = max_address_core1
        self.random_explor = RANDOM(self.N_init,self.env,self.H,min_address_core0,max_address_core0,min_address_core1,max_address_core1,self.num_instructions)
    def take(self,sample:dict,start:int): 
        """Takes the ``start`` first steps from the ``sample`` dictionnary to initialize the exploration. 
        Then the iterator i is set to ``start`` directly
        """
        for key1 in sample['memory_perf']:
            for key2 in sample['memory_perf'][key1].keys():
                shape = sample['memory_perf'][key1][key2].shape
                in_ = np.zeros(shape)
                in_[:start] = sample['memory_perf'][key1][key2][:start]  
                self.H.memory_perf[key1][key2] = in_
        self.H.memory_program["core0"] = sample["memory_program"]["core0"][:start]
        self.H.memory_program["core1"] = sample["memory_program"]["core1"][:start]
        self.H.tab = list(sample['tabular_view'][:start])
        self.start = start
        self.N_init = start
        self.H.j = start
    def __call__(self):
        start_time = time.time()
        """Performs the exploration.
        """
        if self.start==0:
            self.random_explor()
        for i in range(self.N_init,self.N):
            if i%1000==0 or i==self.N-1:
                print(f'step {i}/{self.N-1}')
            if (i-self.N_init)%self.periode==0 and i>=self.N_init:
                m = random.choice([3])
                goal,cond,stats = self.G(self.H,m)
            parameter = self.Pi(goal,self.H,stats,cond)
            observation = self.env(parameter)
            self.H.store({"program":parameter}|observation)
        print(time.time() - start_time)
