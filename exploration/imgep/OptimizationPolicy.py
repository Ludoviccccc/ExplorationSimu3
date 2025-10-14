import random
import numpy as np

import sys
sys.path.append("../../")
from exploration.imgep.mutation import mutate_instruction_sequence, mutate_paire_instructions
from exploration.history import History
from exploration.imgep.features import Features

class OptimizationPolicykNN(Features):
    def __init__(self,
                k=1,
                num_mutations = 1,
                max_len=50,
                num_addr = 20,
                num_bank = 4,
                min_instr = 5,
                max_instr = 50,
                max_cycle = 60):
        super().__init__()
        self.k = k
        self.num_mutations = num_mutations
        self.max_cycle = max_cycle
        self.max_len = max_len
        self.num_bank = num_bank #this attribute is used by Features
        self.num_addr = num_addr
        self.min_instr = min_instr
        self.max_instr = max_instr

    def __call__(self,goal:np.ndarray,H:History, module:int)->dict:
        closest_codes = self.select_closest_codes(H,goal, module) #most promising sample from the history
        output = {'core0':closest_codes['program']['core0'][0],
                'core1':closest_codes['program']['core1'][0]}
        return output
    def mix(self,programs):
        ll = np.random.randint(5,self.max_len)
        mix0, mix1 = mix_instruction_lists(programs["program"]["core0"],ll), mix_instruction_lists(programs["program"]["core1"],ll)
        output = self.light_code_mutation({"core0":mix0[:self.max_len],"core1":mix1[:self.max_len]}) #expansion strategie: small random mutation
        return output 
    def loss(self,goal:np.ndarray, elements:np.ndarray):
        if type(goal)!=float:
            a = goal.reshape(-1,1) 
        else:
            a = np.array([goal]).reshape(-1,1) 
        out = np.sum((a -elements)**2,axis=0)
        return out
    def feature2closest_code(self,features,signature:np.ndarray)->np.ndarray:
        if type(signature)==np.ndarray:
            if features.ndim==1 and (signature.shape[0]>1 or signature.ndim>1):
                raise TypeError(f"goal of shape {signature.shape} has be a float. Features of shape {features.shape}")
        d = self.loss(signature,features)
        idx = np.argsort(d)[:self.k]
        return idx
    def select_closest_codes(self,H:History,signature: np.ndarray,module:int)->dict:
        assert len(H.memory_program)>0, "history empty"
        output = {"program": {"core0":[],"core1":[]},}
        features = H.as_array()[:,module]
        idx = self.feature2closest_code(features,signature)
        for id_ in idx:
            output["program"]["core0"].append(H.memory_program["core0"][id_])
            output["program"]["core1"].append(H.memory_program["core1"][id_])
        return output
    def light_code_mutation(self,programs:dict[list[dict]]):
        mutated0 = mutate_instruction_sequence(programs['core0'],num_mutations=5,max_cycle=self.max_cycle)
        mutated1 = mutate_instruction_sequence(programs['core0'],num_mutations=5,max_cycle=self.max_cycle)
        return mutated0,mutated1
