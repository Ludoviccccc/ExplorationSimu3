import numpy as np
import sys
sys.path.append('../../')
from exploration.history2 import History


class ALP_module:
    '''
    use areas to calculate reward
    '''
    def __init__(self,H:History,
                      window_size = 100):
        self.History = History
        self.window_size = window_size
    def fit(self):
        '''
        fits best gmm models on moving window
        '''
