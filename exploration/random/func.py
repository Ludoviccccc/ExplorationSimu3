import sys
import random
sys.path.append("../../")
sys.path.append("../../simulator")
sys.path.append("../../exploration/")
from exploration.env.func import Env
from exploration.history import History
from codegeneration import generate_instruction_sequence
import random

class RANDOM:
    def __init__(self,N:int,E:Env,H:History,
                    min_address_core0 = 0 ,
                    max_address_core0 = 10,
                    min_address_core1 = 11,
                    max_address_core1 = 21

            ):
        """
        N: int. The experimental budget
        H: History. Buffer containing codes and signature pairs
        max_l: int. Max length for of the instruction sequences
        E: Env. The environnement.
        """
        self.env = E
        self.H = H
        self.N = N
        self.max_cycle = 60
        self.min_address_core0 = min_address_core0
        self.max_address_core0 = max_address_core0
        self.min_address_core1 = min_address_core1
        self.max_address_core1 = max_address_core1
    def __call__(self):
        for i in range(self.N):
            if i%1000==0 or i==self.N-1:
                print(f'step {i}/{self.N-1}')
            code0 = generate_instruction_sequence(None,max_cycle = self.max_cycle,min_address=self.min_address_core0,max_address = self.max_address_core0)
            code1 = generate_instruction_sequence(None,max_cycle = self.max_cycle,min_address=self.min_address_core1,max_address = self.max_address_core1)
            parameter = {'core0':code0,
                        'core1':code1}
            self.H.store({"program":parameter}|self.env(parameter))
