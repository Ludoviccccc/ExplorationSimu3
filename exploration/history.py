import numpy as np
import pickle
import os.path
import copy
class History:
    def __init__(self, max_size = 100):
        self.max_size = max_size
        self.memory_program = {"core0":[],"core1":[]}
        self.memory_perf = {'mutual':{},
                            'core0':{},
                            'core1':{}}
        self.memory_tab = []
    def eviction(self):
        if len(self.memory_program)>self.max_size:
            self.memory_program["core0"] = self.memory_program["core0"][-self.max_size:]
            self.memory_program["core1"] = self.memory_program["core1"][-self.max_size:]
    def purge(self):
        self.memory_program["core0"] = [] 
        self.memory_program["core1"] = []
    def __len__(self):
        return len(self.memory_program["core0"])
    def store(self,sample:dict[list]):
        #print("
        #for j in range(len(sample["program"]["core0"])):
        self.memory_program["core0"].append(sample["program"]["core0"])
        self.memory_program["core1"].append(sample["program"]["core1"])
        for key1 in self.memory_perf.keys():
            for key2 in sample[key1].keys():
                if key2 in self.memory_perf[key1]:
                    self.memory_perf[key1][key2].append(sample[key1][key2])
                else:
                    self.memory_perf[key1][key2] = [sample[key1][key2]]
    def present_content(self):
        output  = {key:np.array(self.memory_perf[key]) for key in self.memory_perf.keys()}
        return output
    def content(self):
        """
        returns dictionary of content
        """
        keys = ['time_core0', 'time_core1', 'miss_ratios_detailled', 'miss_ratios_global', 'L1_miss_ratio_core0', 'L1_miss_ratio_core1', 'L2_miss_ratio']
        return {"memory_perf":{key:{k:np.array(self.memory_perf[key][k]) for k in self.memory_perf[key] if k in keys} for key in self.memory_perf.keys()},
                "memory_program":{"core0":self.memory_program["core0"],"core1":self.memory_program["core1"]}}
    def save_pickle(self, name:str=None):
        k = 0
        while os.path.isfile(f"{name}_{k}.pkl"):
            k+=1
        output = self.content()
        with open(f"{name}_{k}.pkl", "wb") as f:
            pickle.dump(output, f)
    def __getitem__(self,val):
        """
        returns slice of memory_perf and memory_program in this order
        """
        memory_program = {"core0":[],"core1":[]}
        memory_perf = {}
        for k in self.memory_perf.keys():
            memory_perf[k] = self.memory_perf[k][val]
        for k in self.memory_program.keys():
            memory_program[k] = self.memory_program[k][val]
        return memory_perf,memory_program
    def take(self,sample:dict,N_init:int):
        """Takes the ``N_init`` first steps from the ``sample`` dictionnary to initialize the expl    oration. 
        Then the iterator i is set to N_init directly
        """
        print("sampl", sample.keys())
        for key in sample["memory_perf"].keys():
            self.memory_perf[key]= list(sample["memory_perf"][key][:N_init])
        self.memory_program["core0"] = sample["memory_program"]["core0"][:N_init]
        self.memory_program["core1"] = sample["memory_program"]["core1"][:N_init]
    
    def as_array(self):
        keys = ['time_core0', 'time_core1', 'miss_ratios_detailled', 'miss_ratios_global', 'L1_miss_ratio_core0', 'L1_miss_ratio_core1', 'L2_miss_ratio']
        len_ = len(self.memory_perf['core0']['time_core0']) 
        tab = [np.array(self.memory_perf[core][key]).reshape(len_,-1) for key in keys for core in ['core0','core1','mutual'] if key in self.memory_perf[core] ]
        return np.concatenate(tab,axis=1)
