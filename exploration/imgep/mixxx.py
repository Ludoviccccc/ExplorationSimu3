import random

def random_mix_sequences(sequences, seed=None, max_gap=5,max_cycle=60):
    """
    Randomly mix all instructions from multiple sequences, preserving relative timing.

    Args:
        sequences (list[dict]): list of input sequences, each {cycle: (type, address)}
        seed (int, optional): random seed for reproducibility
        max_gap (int): maximum random gap (in cycles) between successive instructions

    Returns:
        dict: new mixed sequence {cycle: (type, address)} with randomized order and timing
    """
    if seed is not None:
        random.seed(seed)

    # Flatten all instructions into a single list [(type, address), ...]
    all_instructions = []
    for seq in sequences:
        all_instructions.extend(list(seq.values()))

    # Randomize instruction order
    random.shuffle(all_instructions)

    # Build new sequence with random cycle gaps
    mixed = {}
    current_cycle = 0
    for op in all_instructions:
        # Random gap between 1 and max_gap cycles
        current_cycle += random.randint(1, max_gap)
        mixed[current_cycle] = op

    out =  dict(sorted(mixed.items()))
    out = {key:out[key] for key in out.keys() if key <= max_cycle}
    return out

#seq1 = {0: ('read', 1), 1: ('write', 2), 3: ('read', 3)}
#seq2 = {2: ('write', 5), 4: ('read', 7)}
#seq3 = {0: ('read', 9), 1: ('write', 10)}
#
#
#
#
#mixed = random_mix_sequences([seq1, seq2, seq3], seed=42, max_gap=4)
#print(mixed)


#from simu3.codegeneration import generate_instruction_sequence
#
#seq1 = generate_instruction_sequence()
#seq2 = generate_instruction_sequence()
#print('seq1',seq1)
#print('seq2',seq2)
#
#mixed = random_mix_sequences([seq1, seq2], seed=42, max_gap=4)
#print(mixed)
