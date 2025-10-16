import random
import numpy as np

import sys
sys.path.append("../../")
from exploration.imgep.mutation import mutate_instruction_sequence, mutate_paire_instructions
from exploration.history import History
from exploration.imgep.features import Features
from exploration.imgep.mix import mix_sequences
from exploration.imgep.mixxx import random_mix_sequences

def subsequence(cycle,parameter):
    '''
    returns the sequences of instructions up to the given cycle
    '''
    return {'core0':{k:parameter['core0'][k] for k in parameter['core0'] if k<=cycle},
     'core1':{k:parameter['core1'][k] for k in parameter['core1'] if k<cycle}}

class OptimizationPolicykNN(Features):
    def __init__(self,
                k=1,
                num_mutations = 1,
                num_addr = 20,
                num_bank = 4,
                min_instr = 5,
                max_instr = 50,
                max_cycle = 60,
                min_address_core0 = 0,
                max_address_core0 = 10,
                min_address_core1 = 11,
                max_address_core1 = 21,
                segment_method=True,
                ):
        super().__init__()
        self.segment_method = segment_method
        self.min_address_core0 = min_address_core0
        self.max_address_core0 = max_address_core0
        self.min_address_core1 = min_address_core1
        self.max_address_core1 = max_address_core1
        self.k = k
        self.num_mutations = num_mutations
        self.max_cycle = max_cycle
        self.num_bank = num_bank #this attribute is used by Features
        self.num_addr = num_addr
        self.min_instr = min_instr
        self.max_instr = max_instr

    def __call__(self,goal:np.ndarray,H:History, module:int)->dict:
        closest_codes = self.select_closest_codes(H,goal, module) #most promising sample from the history
        output = {'core0':closest_codes['program']['core0'],
                'core1':closest_codes['program']['core1']}
        output = self.mix(output)
        output = self.light_code_mutation(output)
        return output
    def mix(self,programs:list[dict]):
        if self.segment_method:
            mix0, mix1 = mix_sequences(programs["core0"],max_cycle=self.max_cycle), mix_sequences(programs["core1"],max_cycle=self.max_cycle)
        else:
            mix0, mix1 = random_mix_sequences(programs["core0"],max_cycle=self.max_cycle), mix_sequences(programs["core1"],max_cycle=self.max_cycle)
        return {'core0':[mix0],'core1':[mix1]}
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
        mutated0 = mutate_instruction_sequence(programs['core0'][0],num_mutations=self.num_mutations,max_cycle=self.max_cycle,min_address=self.min_address_core0,max_address=self.max_address_core0)
        mutated1 = mutate_instruction_sequence(programs['core1'][0],num_mutations=self.num_mutations,max_cycle=self.max_cycle,min_address=self.min_address_core1,max_address=self.max_address_core1)
        return {'core0':mutated0,'core1':mutated1}
