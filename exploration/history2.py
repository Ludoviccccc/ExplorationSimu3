import numpy as np
import pickle
import os.path
import copy
class History:
    def __init__(self,env=None,capacity=1000):
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
        self.reward_vec = [0]
        self.interleaving = np.zeros((self.capacity,4))
    def as_tab(self):
        return np.array(self.tab)
    def __len__(self):
        return len(self.memory_program["core0"])
    def store(self,sample:dict,module:int=None):
        key_set = ['shared_resource_events']
        self.memory_program["core0"].append(sample["program"]["core0"])
        self.memory_program["core1"].append(sample["program"]["core1"])
        observation_vec = []
        step = 5
        k =0
        for key1 in self.memory_perf.keys():
            for key2 in sample[key1].keys():
                if key2 not in key_set:
                    value = np.array(sample[key1][key2]).reshape((-1))
                    observation_vec.append(value)
                    k+=1
                if key2 in self.memory_perf[key1] and key2 not in key_set:
                    self.memory_perf[key1][key2][self.j] = sample[key1][key2]
                elif key2 not in key_set:
                    try:
                        shape = sample[key1][key2].shape
                    except:
                        shape =None
                    if shape:
                        self.memory_perf[key1][key2] = np.zeros((self.capacity,)+sample[key1][key2].shape)
                    else:
                        self.memory_perf[key1][key2] = np.zeros((self.capacity))
                    self.memory_perf[key1][key2][0] = sample[key1][key2]
                # shared resource events
                elif key2 in key_set:
                    if key2 in self.memory_perf[key1] and sample[key1][key2]!=[]:
                        self.memory_perf[key1][key2][self.j] = sample[key1][key2]
                    elif sample[key1][key2]!=[] :
                        self.memory_perf[key1][key2] = {self.j:sample[key1][key2]}
                    if sample[key1][key2]!=[]:
                        for event in sample[key1][key2]:
                            if event['type']=='DDR_MEMORY_CONTENTION':
                                self.shared_resource_list.append(shared_resource2vec(event,self.env))
                                self.shared_resource_coords.append({'program':self.j,'cycle':event['cycle']})
                                self.interleaving[self.j] +=shared_resource2vec(event,self.env)[1:5]
        #synthetizes an array with all observations, usefull for exploration.
        observation_vec = np.concatenate(observation_vec)
        if self.j==0:
            self.reward_vec = np.zeros((self.capacity,len(observation_vec)))
            self.novelty_vec = np.zeros((self.capacity))
        if self.j>0:
            if self.j==1 or self.j%200==0:
                self.weight = np.max(self.as_tab(),axis=0)
                self.weight /=np.sum(self.weight)
            diff = self.as_tab() - observation_vec
            new_novelty = np.mean(np.sum(self.weight*(diff)**2,axis=1))
            closest_points = np.abs(diff).argmin(axis=0)
            self.reward_vec[self.j] = np.abs(new_novelty - self.novelty_vec[closest_points])
            self.novelty_vec[self.j] = new_novelty
        self.tab.append(observation_vec)
        self.j+=1
    def prob(self):
        epsilon = 0.5
        c = self.score
        unif = np.ones(len(c))/len(c)
        if np.sum(self.score)!=0:
            c /=np.sum(self.score)
            return c*(1-epsilon)+epsilon*unif
        else:
            return unif
    def content(self):
        """
        returns dictionary of content
        """
        keys = ['time_core0', 'time_core1', 'miss_ratios_detailled', 'miss_ratios_global', 'L1_miss_ratio_core0', 'L1_miss_ratio_core1', 'L2_miss_ratio']
        return {"memory_perf":{key:{k:np.array(self.memory_perf[key][k]) for k in self.memory_perf[key] if k in keys} for key in self.memory_perf.keys()},
                "memory_program":{"core0":self.memory_program["core0"],"core1":self.memory_program["core1"]},
                "reward":self.reward_vec,
                "tabular_view":self.as_tab(),
                "interleaving":self.interleaving,
                }
    def save_pickle(self, name:str=None):
        k = 0
        while os.path.isfile(f"{name}_{k}.pkl"):
            k+=1
        output = self.content()
        with open(f"{name}_{k}.pkl", "wb") as f:
            pickle.dump(output, f)
    def take(self,sample:dict,N_init:int):
        """Takes the ``N_init`` first steps from the ``sample`` dictionnary to initialize the expl    oration. 
        Then the iterator i is set to N_init directly
        """
        self.j = N_init
        self.memory_perf = sample["memory_perf"]
        self.memory_program["core0"] = sample["memory_program"]["core0"]
        self.memory_program["core1"] = sample["memory_program"]["core1"]
        self.tab = np.concatenate([np.array(sample['memory_perf'][key1][key2]).reshape((N_init,-1)) for key1 in sample['memory_perf'] for key2 in sample['memory_perf'][key1] if key2!='shared_resource_events'],axis=1)    


def shared_resource2vec(in_,E):
    count_banks = np.histogram(in_['details']['banks'],bins = range(E.num_banks+1))[0]#/len(in_['details']['banks'])
    count_rows = np.histogram(in_['details']['rows'],bins = range(E.num_rows+1))[0]#/len(in_['details']['banks'])
    ratios_core = np.array([sum(np.array(in_['initiators'])==1)/len(in_['initiators'])])
    conflicts = np.array([1*in_['details']['bank_conflicts'],1*in_['details']['row_conflicts']])
    out = np.concatenate((ratios_core,count_banks,count_rows,conflicts),axis=0)
    return out
