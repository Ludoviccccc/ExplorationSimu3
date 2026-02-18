import matplotlib.pyplot as plt
import sys
sys.path.append('../../')
from exploration.load_file import load
import numpy as np
import os
import pandas as pd
def row(program):
    rows = np.zeros(3)
    for k in program:
        rows[program[k][1]//16] +=1
    return rows
def bank(program):
    banks = np.zeros(4)
    for k in program:
        banks[program[k][1]%4] +=1
    return banks
def bank_row(program):
    output = np.zeros((4,3))
    for k in program:
        output[program[k][1]%4,program[k][1]//16] +=1
    return output
def diagnostic_plot(content_rand_name,content_names):
    content_rand = load(content_rand_name)
    a_rand = np.array([bank_row(program) for program in content_rand['memory_program']['core0']])
    b_rand = np.array([bank_row(program) for program in content_rand['memory_program']['core1']])
    y_rand_0 = content_rand['memory_perf']['mutual']['diff_time_core0']
    y_rand_1 = content_rand['memory_perf']['mutual']['diff_time_core1']
    c_rand = np.abs(a_rand-b_rand).sum(axis=(1,2))
    print(c_rand.shape)
    for j,vec in enumerate(content_names):
        name = vec[0]
        label = vec[1]
        content = load(name)
        a = np.array([bank_row(program) for program in content['memory_program']['core0']])
        b = np.array([bank_row(program) for program in content['memory_program']['core1']])
        # mesure overlap bank_rows
        c = np.abs(a-b).sum(axis=(1,2))
        y_0 = content['memory_perf']['mutual']['diff_time_core0']
        y_1 = content['memory_perf']['mutual']['diff_time_core1']
        fig,(ax0,ax1) = plt.subplots(1,2,sharex=True,figsize=(12,5))
        ax0.scatter(c,y_0,label=label)
        ax1.scatter(c,y_1,label=label)
        ax0.set_xlabel(f'non-overlap',fontsize=18)
        ax1.set_xlabel(f'non-overlap',fontsize=18)
        ax0.set_ylabel(f'time[mutual] - time[core 0]',fontsize=18)
        ax1.set_ylabel(f'time[mutual] - time[core 1]',fontsize=18)
        plt.legend( prop={'size': 18})
        plt.savefig(os.path.join('images',f'bank_row_delay_{j}'))
        plt.suptitle('Delay vs non-overlap',fontsize=18)
        plt.show()

        data = pd.DataFrame([])
        data['diff_time_core0'] = y_0
        data['diff_time_core1'] = y_1
        data['over_lap'] = c
        data.to_csv("data_diagnostic",header = True)
