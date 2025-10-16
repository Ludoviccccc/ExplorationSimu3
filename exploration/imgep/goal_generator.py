import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
#from exploration.imgep.features import Features
class GoalGenerator:#(Features):
    def __init__(self,
                 ):
        super().__init__()
    def __call__(self,H:History, module:int)->np.ndarray:
        stat = H.as_array()[:,module]
        min_ = stat.min(axis=-1)
        max_ = stat.max(axis=-1)
        if module<=4:
            out = np.random.uniform((1-np.sign(min_)*0.6)*min_,4.0*max_)
        else:
            out = np.random.uniform(min_,max_)
        return out
