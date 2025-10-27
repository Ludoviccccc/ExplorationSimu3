import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
class GoalGenerator:
    def __init__(self,
                 ):
        pass
    def __call__(self,H:History,m:int)->np.ndarray:
        Tab = H.as_tab()
        min_ = Tab.min(axis=0)
        max_ = Tab.max(axis=0)
        cond = None
        if m==0:
            out = np.random.uniform(min_,2*max_*(max_>1)+max_*(max_<=1))
        else:
            if m==1:
                cond = np.where(max_>1.0)[0]
                min_2 = min_[cond]
                max_2 = max_[cond]
                out = np.random.uniform(min_2,2*max_2)
            else:
                cond = np.where(max_<=1.0)[0]
                min_2 = min_[cond]
                max_2 = max_[cond]
                out = np.random.uniform(min_2,max_2)
        return out,cond
