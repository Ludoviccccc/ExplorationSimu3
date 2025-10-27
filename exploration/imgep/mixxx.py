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


import random

def segment_mix_sequences(sequences, num_parts=3, seed=None, max_cycle=60):
    """
    Mix contiguous parts from multiple instruction sequences, preserving timing,
    and ensuring the resulting sequence fits within a maximum cycle range.

    Args:
        sequences (list[dict]): list of input sequences, each {cycle: (type, address)}
        num_parts (int): number of contiguous parts to extract and mix
        seed (int, optional): random seed for reproducibility
        max_cycle (int): maximum allowed cycle for final mixed sequence

    Returns:
        dict: new mixed sequence {cycle: (type, address)}
    """
    if seed is not None:
        random.seed(seed)

    mixed = {}
    current_time = 0

    for _ in range(num_parts):
        # Stop if we’ve reached or exceeded the cycle limit
        if current_time >= max_cycle:
            break

        # Choose a random sequence
        seq = random.choice(sequences)
        if not seq:
            continue

        # Sort cycles
        cycles = sorted(seq.keys())
        if not cycles:
            continue

        # Choose random start
        start = random.choice(cycles)

        # Choose random contiguous slice length
        max_len = len(cycles) - cycles.index(start)
        if max_len <= 0:
            continue
        length = random.randint(1, max_len)

        # Extract contiguous block
        block_cycles = cycles[cycles.index(start):cycles.index(start) + length]
        block = {c: seq[c] for c in block_cycles}

        # Compute relative timing for this block
        min_cycle = block_cycles[0]
        shifted_block = {
            current_time + (c - min_cycle): op for c, op in block.items()
        }

        # Filter out instructions exceeding max_cycle
        shifted_block = {
            c: op for c, op in shifted_block.items() if c <= max_cycle
        }

        # Stop if no valid instruction fits
        if not shifted_block:
            break

        # Add to mixed sequence
        mixed.update(shifted_block)

        # Update current_time with random gap, but not beyond max_cycle
        next_time = max(shifted_block.keys()) + random.randint(1, 5)
        if next_time > max_cycle:
            break
        current_time = next_time

    return dict(sorted(mixed.items()))

