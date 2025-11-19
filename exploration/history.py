import numpy as np
import pickle
import os.path
import copy
class History:
    def __init__(self,env=None,capacity=10000):
        self.memory_program = {"core0":[],"core1":[]}
        self.memory_perf = {'mutual':{},
                            'core0':{},
                            'core1':{}}
        self.j = 0
        self.capacity = capacity
        self.shared_resource_list = []
        self.shared_resource_coords = []
        self.env = env
        self.tab = []
        self.names = []
    def as_tab(self):
        return np.array(self.tab)
    def __len__(self):
        return len(self.memory_program["core0"])
    def store(self,sample:dict,module:int=None):
        self.memory_program["core0"].append(sample["program"]["core0"])
        self.memory_program["core1"].append(sample["program"]["core1"])
        observation_vec = []
        for key1 in self.memory_perf.keys():
            for key2 in sample[key1].keys():
                if self.j==0:
                    self.names.append(key1+'_'+key2)
                value = np.array(sample[key1][key2]).reshape((-1))
                if (key2 in [
                            'miss_read_core0',
                            'miss_read_core1',
                            'hits_read_core0',
                            'hits_read_core1',
                            'miss_write_core0',
                            'miss_write_core1',
                            'hits_write_core0',
                            'hits_write_core1',
                            'diff_time_core0',
                            'diff_time_core1',
                            'diff_time',
                            #'L2_hit_core0',
                            #'L2_hit_core1',
                            #'L2_miss_core0',
                            #'L2_miss_core1'
                            ]+[f'L2_{c}_{type_}_{core}' for c in ['miss','hit'] for type_ in ['write','read'] for core in ['core0','core1']]):
                    observation_vec.append(value)
                if self.j==0:
                    self.names +=[key1+'_'+key2]*len(value)
                if self.j==0:
                    try:
                        shape = sample[key1][key2].shape
                        self.memory_perf[key1][key2] = np.zeros((self.capacity,)+sample[key1][key2].shape)
                    except:
                        shape =None
                        self.memory_perf[key1][key2] = np.zeros((self.capacity))
                self.memory_perf[key1][key2][self.j] = sample[key1][key2]
        #synthetizes an array with all observations, usefull for exploration.
        observation_vec = np.concatenate(observation_vec)
        self.tab.append(observation_vec)
        self.j+=1
    def content(self):
        """
        returns dictionary of content
        """
        return {"memory_perf":self.memory_perf,
                "memory_program":self.memory_program,
                "tabular_view":self.as_tab(),
                "names":self.names}
    def save_pickle(self, name:str=None):
        k = 0
        while os.path.isfile(f"{name}_{k}.pkl"):
            k+=1
        output = self.content()
        with open(f"{name}_{k}.pkl", "wb") as f:
            pickle.dump(output, f)
