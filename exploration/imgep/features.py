import numpy as np
class Features:
    def __init__(self):
        pass
    def data2feature(self,stats:dict,module:str)->np.ndarray:
        assert type(module)==dict,f'wrong type:{type(module)}'
        if module['type']=='time_vector':
            out = np.stack((stats['core0']['time_core0'],
                            stats['core1']['time_core1'],
                            stats['mutual']['time_core0'],
                            stats['mutual']['time_core1'],
                            ))
        elif module['type']=='time':
            out = stats[module['core']][module['var']]
        elif module['type']=='miss_ratios_detailled':
            bank = module['bank']
            row = module['row']
            core = module['core']
            out = np.array(stats[core][f'miss_ratios_detailled'])[:,row,bank]
        elif module['type']=='vec_miss_ratios_detailled':
            core = module['core']
            out = np.array(stats[core][f'miss_ratios_detailled'])
        elif module['type']=='cache_miss_ratio':
            core = module['core']
            level = module['level']
            out = stats[f'core{core}_{level}_cache_miss'][:,module['addr']]
            #print('out', np.array(out))
            #exit()
        elif module['type']=='shared_cache_miss_ratio':
            out = np.array(stats[f'shared_cache_miss'])
            out = out[:,module['addr']]
        elif module['type']=='general_shared_cache_miss':
            out = np.array(stats[f'general_shared_cache_miss'])
        elif module['type']=='general_shared_cache_miss_core0':
            out = np.array(stats[f'general_shared_cache_miss_core0'])
        elif module['type']=='general_shared_cache_miss_core1':
            out = np.array(stats[f'general_shared_cache_miss_core1'])
        else:
            TypeError(f'module {module} unknown')
        return np.array(out)
