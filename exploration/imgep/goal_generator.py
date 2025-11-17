import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
class GoalGenerator:
    def __init__(self,):
        pass
    def __call__(self,H:History)->np.ndarray:
        Tab = H.as_tab()
        min_ = Tab.min(axis=0)
        max_ = Tab.max(axis=0)
        out = np.random.uniform(.6*min_,1.4*max_)
        return out,{'min':min_,'max':max_}
