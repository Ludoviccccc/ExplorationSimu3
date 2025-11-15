import random
import numpy as np

import sys
sys.path.append("../../")
from exploration.imgep.mutation import mutate_instruction_sequence
from exploration.history import History
from exploration.imgep.mix import mix_sequences
from exploration.imgep.mixxx import random_mix_sequences,segment_mix_sequences
from exploration.test_addr import test_programs
def subsequence(cycle,parameter:dict):
    '''
    returns the sequences of instructions up to the given cycle
    '''
    return {k:parameter[k] for k in parameter if k<=cycle}

class OptimizationPolicykNN(test_programs):
    def __init__(self,
                k=1,
                num_mutations = 1,
                max_cycle = 60,
                min_address_core0 = 0,
                max_address_core0 = 10,
                min_address_core1 = 11,
                max_address_core1 = 21,
                segment_method=True,
                num_instructions=None,
                ):
        super().__init__()
        self.segment_method = segment_method
        self.min_address_core0 = min_address_core0
        self.max_address_core0 = max_address_core0
        self.min_address_core1 = min_address_core1
        self.max_address_core1 = max_address_core1
        self.k = k
        self.j = 0#counter to fix self.sup and self.inf
        self.num_mutations = num_mutations
        self.max_cycle = max_cycle
        self.num_instructions = num_instructions
    def __call__(self,goal:np.ndarray,H:History,stats:dict)->dict:
        closest_codes = self.select_closest_codes(H,goal,stats) #most promising sample from the history
        output = {'core0':closest_codes['program']['core0'],
                'core1':closest_codes['program']['core1']}
        if self.k>1:
            output = self.mix(output)
        output = self.light_code_mutation(output)
        return output
    def mix(self,programs:list[dict]):
        if not self.segment_method:
            mix0 = mix_sequences(programs["core0"],max_cycle=self.max_cycle)
            mix1 = mix_sequences(programs["core1"],max_cycle=self.max_cycle)
        else:
            mix0 = segment_mix_sequences(programs["core0"],max_cycle=self.max_cycle)
            mix1 = segment_mix_sequences(programs["core1"],max_cycle=self.max_cycle)
        return {'core0':[mix0],'core1':[mix1]}
    def loss(self,goal:np.ndarray, elements:dict):
        a = np.array([goal]).reshape(1,-1)#size (dim,N), N=1 individual
        max_ = elements['max']
        min_ = elements['min']
        out = np.sum(((a - elements['features']))**2,axis=1)
        return out
    def feature2closest_code(self,features:dict,signature:np.ndarray)->np.ndarray:
        d = self.loss(signature,features)
        idx = np.argsort(d)[:self.k]
        return idx
    def select_closest_codes(self,H:History,signature: dict,stats:dict)->dict:
        assert len(H.memory_program)>0, "history empty"
        output = {"program": {"core0":[],"core1":[]},}
        features = H.as_tab()
        idx = self.feature2closest_code({'features':features}|stats,signature)
        for id_ in idx:
            output["program"]["core0"].append(H.memory_program["core0"][id_])
            output["program"]["core1"].append(H.memory_program["core1"][id_])
        return output
    def light_code_mutation(self,programs:dict[list[dict]]):
        mutated0 = mutate_instruction_sequence(programs['core0'][0],
                        num_mutations=self.num_mutations,
                        max_cycle=self.max_cycle,
                        min_address=self.min_address_core0,
                        max_address=self.max_address_core0,
                        num_instructions=self.num_instructions)
        mutated1 = mutate_instruction_sequence(programs['core1'][0],
                        num_mutations=self.num_mutations,
                        max_cycle=self.max_cycle,
                        min_address=self.min_address_core1,
                        max_address=self.max_address_core1,
                        num_instructions=self.num_instructions)
        self._test_program_addr(mutated0,mutated1) 
        return {'core0':mutated0,'core1':mutated1}
