import numpy as np
import sys
sys.path.append('../../')
from exploration.imgep.ball_areas import BallCloud1D
#from 


class ALP_module:
    '''
    use areas to calculate reward
    '''
    def __init__(self):
        pass
    def reward(self,goal,result):
        '''
        This methods calculates the scalar reward obtained after obtaining vector `result' when targeting vector 'goal'
        '''
        output = (goal-result)**2
        return output
