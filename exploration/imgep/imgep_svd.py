import sys
sys.path.append("../")
sys.path.append("../../")
from exploration.env.func import Env
from exploration.history import History
from exploration.imgep.OptimizationPolicy import OptimizationPolicykNN
from exploration.imgep.imgep import IMGEP
import random
from codegeneration import generate_instruction_sequence
from exploration.random.func import RANDOM
import numpy as np

class OptimizationPolicykNN_(OptimizationPolicykNN):
    def __init__(self,
                k=1,
                num_mutations =1,
                num_addr = 20,
                num_bank = 4,
                max_cycle = 60,
                min_address_core0 = 0,
                max_address_core0 = 10,
                min_address_core1 = 11,
                max_address_core1 = 21,
                segment_method=True,
                ):
            super(OptimizationPolicykNN_,self).__init__(
            k=k,
            num_mutations = num_mutations,
            num_addr = num_addr,
            num_bank = num_bank,
            max_cycle=max_cycle,
            min_address_core0=min_address_core0,
            max_address_core0=max_address_core0,
            min_address_core1=min_address_core1,
            max_address_core1=max_address_core1,
            segment_method=segment_method,
            )
    def select_closest_codes(self,H,coords:np.ndarray,goal:np.ndarray):
        idx = self.feature2closest_code(coords.reshape((1,-1)),goal)
        output = {"core0":[],"core1":[]}
        for id_ in idx:
            output["core0"].append(H.memory_program["core0"][id_])
            output["core1"].append(H.memory_program["core1"][id_])
        return output
    def __call__(self,goal:np.ndarray,H:History,coords:np.ndarray)->dict:
        closest_codes = self.select_closest_codes(H,coords,goal) #most promising sample from the h    istory
        output = self.mix(closest_codes) #expansion strategie: small random mutation
        output = self.light_code_mutation(output)
        return output
    

class GoalGenerator:
    def __init__(self,
                 ):
        pass
    def __call__(self,Feature:np.array, module:int)->np.ndarray:
        min_ = Feature[:,module].min(axis=-1)
        max_ = Feature[:,module].max(axis=-1)
        if module<=4:
            out = np.random.uniform((1-np.sign(min_)*0.6)*min_,4.0*max_)
        else:
            out = np.random.uniform(min_,max_)
        return out


class Normalize:
    """Affine normalization
    """
    def __init__(self):
        self.min_=None
        self.max_= None
        self.g = 1
    def fit(self,x):
        self.min_ = x.min(axis=0)
        self.max_ = x.max(axis=0)
        self.g=0
    def transform(self,x):
        if self.g:
            raise TypeError(f"User must call method Normalize.fit before calling method Normalize.    transform")
        return (x - self.min_)/(self.max_-self.min_)


class IMGEP_SVD(IMGEP):
    def __init__(self,
                 N:int,
                 N_init:int,
                 E:Env,
                 H:History,
                 G:GoalGenerator, 
                 Pi:OptimizationPolicykNN_,
                 Norm:Normalize,
                 periode:int = 1,
                 ):
        super(IMGEP_SVD,self).__init__(N=N,
                                   N_init=N_init,
                                   E=E,
                                   H=H,
                                   G=G,
                                   Pi=Pi,
                                   periode = periode)
        self.norm = Norm
        self.N = N
        self.env = E
        self.H = H
        self.G = G
        self.N_init = N_init
        self.Pi = Pi
        self.periode = periode
        self.start = 0
        self.random_explor = RANDOM(self.N_init,self.env,self.H)
    def __call__(self):
        """Performs the exploration.
        """
        if self.start==0:
            self.random_explor()
        for i in range(self.N_init,self.N+1):
            if i%1000==0:
                print(f'step {i}/{self.N-1}')
            if i%(self.periode*10)==0 or i==self.N_init:
                in_ = self.H.as_tab()
                self.norm.fit(in_)
                in_0 = self.norm.transform(in_)
                U,sigma,Vh =np.linalg.svd(in_0)
            if i%self.periode==0 or i==self.N_init:
                idx_axis = np.random.randint(0,in_.shape[1])
            in_ = self.H.as_array()
            coords = self.norm.transform(in_)@Vh.transpose()
            goal = self.G(coords,idx_axis)
            parameter = self.Pi(goal,self.H, coords[:,idx_axis])
            observation = self.env(parameter)
            self.H.store({"program":parameter}|observation)
