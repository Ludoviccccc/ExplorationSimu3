from exploration.load_file import load
import numpy as np
import os

class test_bij:
    def __init__(self):
        self.num_banks = 4
    def _get_bank(self, addr):
        return addr % self.num_banks

    def _get_row(self, addr):
        return addr // 16 # Example: each row     covers 16 addresses (line_size is 4, so 4 cach    e lines per row for a 4-line_size cache)


folder = 'results'
path = os.path.join(folder,'imgep_run_1_10000')
content = load(path)
diff_time_core1 = content['memory_perf']['mutual']['diff_time_core1']
print('len',len(diff_time_core1))
argmin_core1 = np.argmin(diff_time_core1)
print('core 1 mutual',content['memory_perf']['mutual']['time_core1'][argmin_core1])
print('core 1 iso',content['memory_perf']['core1']['time_core1'][argmin_core1])
tt = test_bij()
seq0 = content['memory_program']['core0'][argmin_core1]
seq1 = content['memory_program']['core1'][argmin_core1]
bank_row_seq = lambda seq:{cycle:(tt._get_bank(seq[cycle][1]),tt._get_row(seq[cycle][1])) for cycle in seq}
r_b_seq0 = bank_row_seq(seq0)
r_b_seq1 = bank_row_seq(seq1)
print('core0',r_b_seq0)
print('core1',r_b_seq1)


