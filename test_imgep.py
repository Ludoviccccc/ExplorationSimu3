from simulator.sim3 import *
from exploration.env.func import Experiment, Env
from exploration.random.func import RANDOM
import numpy as np
from codegeneration import generate_instruction_sequence
from simulator.sim3 import print_contention_analysis
import pandas as pd
from exploration.history import History
from exploration.imgep.OptimizationPolicy import OptimizationPolicykNN as OP
from exploration.imgep.goal_generator import GoalGenerator
from exploration.imgep.imgep import IMGEP


from visu import comparaison3
if __name__=='__main__':
    N = 10000
    H_rand = History()
    E =Env(300)
    random_explor = RANDOM(N,E,H_rand)
    random_explor()
    H_rand.save_pickle('data_explor/random_run0.pickle')
    tab = H_rand.as_array()
    content_rand = H_rand.content()
    G = GoalGenerator()
    #test optimized policy
    module = 1
    Pi = OP(num_mutations = 3)
    goal = G(H_rand,module)
    theta = Pi(goal,H_rand,module)
    #test imgep
    N_init = 1000
    H = History()
    imgep = IMGEP(N,N_init,E,H,G,Pi)
    imgep()
    tab = H.as_array()
    #print('tab',tab[:,0])
    #imgep.memory_perf['mutual'].keys
    H.save_pickle('data_explor/imgep_run0.pickle')
    content_imgep = H.content()
    
    comparaison3(content_rand['memory_perf'],content_imgep['memory_perf'], ['miss_ratios','time'])
    
