import random
import copy

import copy
from typing import List, Dict, Any

def mutate_paire_instructions(instructions1:list[dict],
                              instructions2:list[dict],
                              mutation_rate=.3,
                              num_addr=20,
                              min_instr:int=5,
                              max_instr:int=50
                              )->(dict,dict):
    return mutate_instructions(instructions1, mutation_rate=mutation_rate,num_addr=num_addr,min_instr=min_instr),mutate_instructions(instructions2, mutation_rate=mutation_rate, num_addr=num_addr,min_instr=min_instr,max_instr=max_instr)

def mutate_instructions(instructions:list[dict],
                        mutation_rate:float=0.3,
                        num_addr:int=20,
                        min_instr:int=5,
                        max_instr:int=50):
    """
    Randomly mutate a list of instructions by:
    1. Changing existing instructions
    2. Deleting instructions
    3. Adding new instructions
    
    
    Args:
        instructions: List of instruction dictionaries
        mutation_rate: Probability of each mutation occurring (0.0 to 1.0)
    
    Returns:
        A new mutated list of instructions
    """
    mutated = []
    for instr in copy.deepcopy(instructions):
        mutated.append(instr)
    
    # Now perform random mutations
    num_mutations = max(0, int(len(mutated) * mutation_rate))
    #num_mutations = 1
    
    for _ in range(num_mutations):
        choices = ['change']
        #################
        if len(mutated)>min_instr:
            choices.append('delete')
        if len(mutated)<=max_instr:
            choices.append('add')
        #################
        mutation_type = random.choice(choices)
        if mutation_type == 'change' and len(mutated) > 0:
            idx = random.randint(0, len(mutated) - 1)
            instr = mutated[idx]
            
            if instr['type']!='nop':
                change_what = random.choice(['type', 'addr'])
            else:
                change_what = 'type'
            if change_what == 'type':
                if instr['type'] =='w':
                    instr['type'] = random.choice(['r','nop'])
                elif instr['type'] =='r':
                    instr['type'] = random.choice(['w','nop'])
                elif instr['type'] =='nop':
                    instr['type'] = random.choice(['w','r'])

                if instr['type'] == 'w':
                    if 'value' not in instr:
                        instr['value'] = random.randint(0, 1000)
                    if 'addr' not in instr:
                        instr['addr'] = random.randint(0, num_addr)


                elif instr['type'] == 'r':
                    if 'value' in instr:
                        del instr['value']
                    if 'addr' not in instr:
                        instr['addr'] = random.randint(0, num_addr)
                elif instr['type'] =='nop':
                    if 'value' in instr:
                        del instr['value']
                    if 'addr' in instr:
                        del instr['addr']
            elif change_what == 'addr':
                instr['addr'] = random.randint(0, num_addr)
            
            elif change_what == 'value' and instr['type'] == 'w':
                instr['value'] = random.randint(0, 1000)
            
        
        elif mutation_type == 'delete' and len(mutated) > 1:
            instr['type']='nop'
            if 'value' in instr:
                del instr['value']
            if 'addr' in instr:
                del instr['addr']
        
        #elif mutation_type == 'add':
        #    new_instr = {}
        #    new_instr['type'] = random.choice(['r', 'w','nop'])
        #    if new_instr['type'] in ['r','w']:
        #        new_instr['addr'] = random.randint(0, num_addr)
        #    new_instr['core'] = instructions[0]["core"]
        #    
        #    if new_instr['type'] == 'w':
        #        new_instr['value'] = random.randint(0, 1000)
        #    pos = random.randint(0, len(mutated))
        #    mutated.insert(pos, new_instr)
    return mutated





#def mix_instruction_lists(instruction_lists: List[List[Dict[str, Any]]],
#                         max_length: int = None) -> List[Dict[str, Any]]:
#    """
#    Mix multiple instruction lists to create a new combined list.
#
#    Args:
#        instruction_lists: List of instruction lists to mix from
#        max_length: Maximum length of the resulting list (None for no limit)
#
#    Returns:
#        A new list of instructions randomly selected from all input lists
#    """
#    if len(instruction_lists)==1: 
#        return instruction_lists[0]
#    sanitized_lists = []
#    for instr_list in instruction_lists:
#        sanitized = []
#        for instr in copy.deepcopy(instr_list):
#            sanitized.append(instr)
#        sanitized_lists.append(sanitized)
#
#    # Flatten all instructions with their source list index
#    all_instructions = []
#    for list_idx, instr_list in enumerate(sanitized_lists):
#        for instr_idx, instr in enumerate(instr_list):
#            all_instructions.append((list_idx, instr_idx, instr))
#
#    if not all_instructions:
#        return []
#
#    # Determine target length
#    if max_length is None:
#        # Use average length of input lists
#        lengths = [len(lst) for lst in sanitized_lists]
#        target_length = int(sum(lengths) / len(lengths))
#    else:
#        target_length = max_length
#
#    # Create new mixed list
#    mixed = []
#    while len(mixed) < target_length and all_instructions:
#        # Randomly select an instruction from all available
#        selected = random.choice(all_instructions)
#        list_idx, instr_idx, instr = selected
#
#        # Add to new list
#        mixed.append(copy.deepcopy(instr))
#
#        # Optionally remove this instance from available choices
#        # to avoid duplicates if desired
#        # all_instructions.remove(selected)
#
#    return mixed
#
import copy
from typing import List, Dict, Any

def mix_instruction_lists(instruction_lists: List[List[Dict[str, Any]]],max_len) -> List[Dict[str, Any]]:
    """
    Mix instruction lists while preserving their original ordering.
    The output length matches the shortest input list.
    Instructions are selected in round-robin fashion from the input lists.

    Args:
        instruction_lists: List of instruction lists to mix from

    Returns:
        A new list of instructions with preserved ordering from inputs
    """
    # First replace all functions with lambda val: None in all input lists
    sanitized_lists = []
    for instr_list in instruction_lists:
        sanitized = []
        for instr in copy.deepcopy(instr_list):
            if instr['type'] == 'r' and 'func' in instr:
                instr['func'] = lambda val: None
            sanitized.append(instr)
        sanitized_lists.append(sanitized)

    # Determine the minimum length
    min_length = min(len(lst) for lst in sanitized_lists) if sanitized_lists else 0

    # Create the mixed list by selecting instructions in order
    mixed = []
    for i in range(min_length):
        # Round-robin through each list at position i
        for lst in sanitized_lists:
            if i < len(lst):
                mixed.append(copy.deepcopy(lst[i]))

    return mixed

