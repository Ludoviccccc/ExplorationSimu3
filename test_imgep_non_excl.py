from exploration.env.func import Env
from exploration.random.func import RANDOM
from exploration.history import History
from exploration.imgep.OptimizationPolicy import OptimizationPolicykNN as OP
from exploration.imgep.goal_generator import GoalGenerator as G
from exploration.imgep.imgep import IMGEP
from exploration.load_file import load
import pickle
import os

if __name__=="__main__":

    N = 10000
    N_init = 1000
    k_values = [1,2,5,10,20,30,40]
    num_mutations = 5
    periode = 1
    min_address_core0 = 0
    max_address_core0 = 20
    min_address_core1 = 21
    max_address_core1 = 40
    num_instructions = 10
    folder = 'non_exclusive_axis_exploration'
    E =Env(400,num_addr=100)
    H_rand = History(env=E,capacity=N)
    #random = RANDOM(N,
    #                E,
    #                H_rand,
    #                min_address_core0,
    #                max_address_core0,
    #                min_address_core1,
    #                max_address_core1,
    #                num_instructions)
    #random()
    #H_rand.save_pickle(f'{folder}/rand_run_{N}')
    name = f'{folder}/rand_run_{N}'
    content_rand = load(name)
    for segment_method in [True]:
        for k in k_values:
            print('k',k)
            print('segment mixing method', segment_method)
            E =Env(400,num_addr=100)
            H = History(env=E,capacity=N)
            Pi = OP(num_mutations = num_mutations,
                    k=k,
                    segment_method=segment_method,
                    min_address_core0=min_address_core0,
                    max_address_core0=max_address_core0,
                    min_address_core1=min_address_core1,
                    max_address_core1=max_address_core1,
                    num_instructions=num_instructions)
            goal_generator = G()
            imgep = IMGEP(N,N_init,E,H,goal_generator,Pi, periode = periode,
                          min_address_core0=min_address_core0,
                          max_address_core0=max_address_core0,
                          min_address_core1=min_address_core1,
                          max_address_core1=max_address_core1,
                          num_instructions=num_instructions)
            imgep.take(content_rand,N_init)
            imgep()
            s = 1 if segment_method else 0
            H.save_pickle(f'{folder}/imgep_run_{k}_{N}_s_{s}')
