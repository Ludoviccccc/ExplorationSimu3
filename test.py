import sys
sys.path.append('../')
sys.path.append('../../')
from exploration.env.func import Env
from exploration.random.func import RANDOM
from exploration.random2.func import OPERATORS
from exploration.history import History
from exploration.imgep.OptimizationPolicy import OptimizationPolicykNN as OP
from exploration.imgep.goal_generator import GoalGenerator as G
from exploration.imgep.imgep import IMGEP
from exploration.load_file import load
import pickle
import os
import json
import time

if __name__=="__main__":
    with open(sys.argv[1],"rb") as f:
        config = json.load(f)
    num_run = config['num_run']
    N = config['N']
    N_init = config['N_init']
    k_values = config['k_values']
    num_mutations = config['num_mutations']
    periode = config['periode']
    min_address_core0 = config['min_address_core0']
    max_address_core0 = config['max_address_core0']
    min_address_core1 = config['min_address_core1']
    max_address_core1 = config['max_address_core1']
    num_parts = config['num_parts']
    num_instructions  = config['num_instructions']
    num_addr = config['num_addr']
    num_addr = config['num_addr']
    folder = 'results'
    os.system(f'mkdir {folder}')
    start_time = time.time()
    for _ in range(num_run):
        E =Env(500,num_addr=num_addr)
        H_rand = History(env=E,capacity=N)
        random = RANDOM(N,
                        E,
                        H_rand,
                        min_address_core0,
                        max_address_core0,
                        min_address_core1,
                        max_address_core1,
                        num_instructions)
        random()
        H_rand.save_pickle(f'{folder}/rand_run_{N}')
        name = f'{folder}/rand_run_{N}'
        content_rand = load(name)
        for k in k_values:
            print('k',k)
            E =Env(500,num_addr=num_addr)
            H = History(env=E,capacity=N)
            Pi = OP(num_mutations = num_mutations,
                    k=k,
                    min_address_core0=min_address_core0,
                    max_address_core0=max_address_core0,
                    min_address_core1=min_address_core1,
                    max_address_core1=max_address_core1,
                    num_parts = num_parts,
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
            H.save_pickle(f'{folder}/imgep_run_{k}_{N}')

            E =Env(500,num_addr=num_addr)
            H_operators = History(env=E,capacity=N)
            operators = OPERATORS(N,
                            N_init,
                            k,
                            num_parts,
                            num_mutations,
                            E,
                            H_operators,
                            min_address_core0,
                            max_address_core0,
                            min_address_core1,
                            max_address_core1,
                            num_instructions)
            operators.take(content_rand,N_init)
            operators()
            H_operators.save_pickle(f'{folder}/operators_run_{k}_{N}')
    print('Total time:',(time.time() - start_time)//3600,'H',((time.time()-start_time)%3600)//60,'m',f"{(time.time()-start_time)%3600%60:.2f}",'s')
