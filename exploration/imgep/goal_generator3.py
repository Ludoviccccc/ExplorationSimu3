import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history2 import History
class GoalGenerator:
    def __init__(self,
                 ):
        self.nb_elem = 3
        self.j = 0
    def __call__(self,H:History,m:int)->np.ndarray:

        Tab = H.as_tab()
        dim = Tab.shape[1]
        min_ = Tab.min(axis=0)
        max_ = Tab.max(axis=0)
        if self.j ==0:
            self.inf = max_<=1.0
            self.sup = max_>1.0
            self.j+=1
        cond = None
        if m==0:
            out = np.random.uniform(0,3*max_*self.sup +1.0*self.inf*max_)
        else:
            if m==1:
                cond = np.where(self.sup)[0]
                min_ = min_[cond]
                max_ = max_[cond]
                out = np.random.uniform(0,max_*200)
            elif m==2:
                cond = np.where(self.inf)[0]
                min_ = min_[cond]
                max_ = max_[cond]
                out = np.random.uniform(0,max_)
            elif m==3:
                cond = np.array(random.sample(range(dim),random.randint(1,self.nb_elem)))
                min_ = min_[cond]
                max_ = max_[cond]
                out = np.random.uniform(min_,max_)
        return out,cond,{'min':min_,'max':max_}
