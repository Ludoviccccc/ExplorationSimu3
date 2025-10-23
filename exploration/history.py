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
        self.hist_vec = []
        self.diversity_vec = []
        self.reward_vec = [0]
        self.alp_vec = [0]
        self.window_size = 200
        self.window = {'id':[],'alp':[]}
    def as_tab(self):
        return np.array(self.tab)
    def __len__(self):
        return len(self.memory_program["core0"])
    def store(self,sample:dict):
        key_set = ['shared_resource_events']
        self.memory_program["core0"].append(sample["program"]["core0"])
        self.memory_program["core1"].append(sample["program"]["core1"])
        observation_vec = []
        diversity = 0
        observation_diversity_vec = []
        step = 5
        k =0
        for key1 in self.memory_perf.keys():
            for key2 in sample[key1].keys():
                if key2 not in key_set:
                    value = np.array(sample[key1][key2]).reshape((-1))
                    observation_vec.append(value)
                    if self.j==0:
                        if key2 in ['time_core0', 'time_core1']:
                            hist = np.zeros((value.shape[0],300//step+1))
                            hist[range(value.shape[0]),int(value//step)]=1
                        else:
                            hist = np.zeros((value.shape[0],21))
                            hist[range(value.shape[0]),value.astype('int64')*100//step]=1
                        self.hist_vec.append(hist)
                    else:
                        if key2 in ['time_core0', 'time_core1']:
                            self.hist_vec[k][range(value.shape[0]),int(value//step)]+=1
                        else:
                            value = 100*value//step
                            self.hist_vec[k][range(value.shape[0]),value.astype('int64')]+=1
                    diversity+=np.sum(self.hist_vec[k]>0)
                    #observation_diversity_vec.append(np.sum(self.hist_vec[k]>0))
                    k+=1
                if key2 in self.memory_perf[key1] and key2 not in key_set:
                    self.memory_perf[key1][key2][self.j] = sample[key1][key2]
                elif key2 not in key_set:
                    try:
                        shape = sample[key1][key2].shape
                    except:
                        shape =None
                    if shape:
                        self.memory_perf[key1][key2] = np.zeros((self.capacity+1,)+sample[key1][key2].shape)
                    else:
                        self.memory_perf[key1][key2] = np.zeros((self.capacity+1))
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
#        if self.j ==0:
#            o = np.concatenate(observation_vec)
#            print('len', len(o))
#            print(o.shape)
#            self.tab = np.zeros((self.capacity,len(o)))
#            self.tab[0] = o
#        else:
#            self.tab[self.j] = np.concatenate(observation_vec)
        observation_vec = np.concatenate(observation_vec)
        self.tab.append(observation_vec)
#        print(self.as_tab().shape)
        if self.j>0:
            self.reward_vec.append(int(diversity - self.diversity_vec[-1]))
        self.diversity_vec.append(int(diversity))
        #calcul observation plus proche
        if self.j>0:
            loss = np.sum((self.as_tab()[:-1]-observation_vec.reshape(1,-1))**2,axis=1)
            alp_value = np.abs(self.reward_vec[loss.argmin()]- self.reward_vec[-1])
            self.alp_vec.append(alp_value)
            self.window['alp'].append(self.alp_vec)
            self.window['id'].append(self.j)
            del self.window['alp'][:-self.window_size]
            del self.window['id'][:-self.window_size]


        self.j+=1
    def content(self):
        """
        returns dictionary of content
        """
        keys = ['time_core0', 'time_core1', 'miss_ratios_detailled', 'miss_ratios_global', 'L1_miss_ratio_core0', 'L1_miss_ratio_core1', 'L2_miss_ratio']
        return {"memory_perf":{key:{k:np.array(self.memory_perf[key][k]) for k in self.memory_perf[key] if k in keys} for key in self.memory_perf.keys()},
                "memory_program":{"core0":self.memory_program["core0"],"core1":self.memory_program["core1"]},
                "reward":self.reward_vec,
                "diversity_vec":self.diversity_vec,
                "alp_vec":self.alp_vec}
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
    count_banks = np.histogram(in_['details']['banks'],bins = range(E.num_banks+1))[0]/len(in_['details']['banks'])
    count_rows = np.histogram(in_['details']['rows'],bins = range(E.num_rows+1))[0]/len(in_['details']['banks'])
    ratios_core = np.array([sum(np.array(in_['initiators'])==1)/len(in_['initiators'])])
    conflicts = np.array([1*in_['details']['bank_conflicts'],1*in_['details']['row_conflicts']])
    out = np.concatenate((ratios_core,count_banks,count_rows,conflicts),axis=0)
    return out
