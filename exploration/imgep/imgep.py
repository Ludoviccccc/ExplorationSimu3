import sys
sys.path.append("../")
sys.path.append("../../")
from exploration.env.func import Env
from exploration.history import History
from  exploration.imgep.OptimizationPolicy import OptimizationPolicykNN
from exploration.imgep.goal_generator import GoalGenerator
import random

from codegeneration import generate_instruction_sequence
from exploration.random.func import RANDOM
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
                ):
        self.N = N
        self.env = E
        self.H = H
        self.G = G
        self.N_init = N_init
        self.Pi = Pi
        self.periode = periode
        self.modules = None
        self.start = 0
        self.random_explor = RANDOM(self.N_init,self.env,self.H,min_address_core0,max_address_core0,min_address_core1,max_address_core1)
    def take(self,sample:dict,start:int): 
        """Takes the ``start`` first steps from the ``sample`` dictionnary to initialize the exploration. 
        Then the iterator i is set to ``start`` directly
        """
        self.start = start
        self.H.memory_perf = sample["memory_perf"]
        self.H.memory_program["core0"] = sample["memory_program"]["core0"]
        self.H.memory_program["core1"] = sample["memory_program"]["core1"]
    def __call__(self):
        """Performs the exploration.
        """
        if self.start==0:
            self.random_explor()
        self.modules = range(self.H.as_tab().shape[1]+1)#average data + shared events
        for i in range(self.N_init,self.N):
            if i%1000==0 or i==self.N-1:
                print(f'step {i}/{self.N-1}')
            if (i-self.N_init)%self.periode==0 and i>=self.N_init:
                module = random.choice(self.modules)
                goal = self.G(self.H, module = module)
            parameter = self.Pi(goal,self.H, module)
            observation = self.env(parameter)
            self.H.store({"program":parameter}|observation)
