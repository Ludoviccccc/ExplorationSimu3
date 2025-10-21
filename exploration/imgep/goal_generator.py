import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
class GoalGenerator:
    def __init__(self,
                 ):
        pass
    def __call__(self,H:History, module:int)->np.ndarray:
        Tab = H.as_tab()
        if module ==Tab.shape[1]:
            min_ = np.array(H.shared_resource_list).min(axis=0)
            max_ = np.array(H.shared_resource_list).max(axis=0)
        else:
            stat = Tab[:,module]
            min_ = stat.min(axis=-1)
            max_ = stat.max(axis=-1)
        if np.max(max_)>1.0:
            out = np.random.uniform((1-np.sign(min_)*0.6)*min_,2.0*max_)
        else:
            out = np.random.uniform(min_,max_)
        return out
