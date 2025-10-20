import numpy as np

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
