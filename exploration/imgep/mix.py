#import random

#def mix_sequences(sequences, num_parts=4, seed=None):
#    """
#    Mix contiguous parts from multiple instruction sequences, preserving timing.
#
#    Args:
#        sequences (list[dict]): list of input sequences, each {cycle: (type, address)}
#        num_parts (int): number of contiguous parts to extract and mix
#        seed (int, optional): random seed for reproducibility
#
#    Returns:
#        dict: new mixed sequence {cycle: (type, address)}
#    """
#    if seed is not None:
#        random.seed(seed)
#
#    mixed = {}
#    current_time = 0
#
#    for _ in range(num_parts):
#        # Choose a random sequence
#        seq = random.choice(sequences)
#        if not seq:
#            continue
#
#        # Sort by cycle
#        cycles = sorted(seq.keys())
#        start = random.choice(cycles)
#
#        # Choose a random contiguous slice length (between 2 and remaining cycles)
#        max_len = len(cycles) - cycles.index(start)
#        if max_len <= 1:
#            continue
#        length = random.randint(1, max_len)
#
#        # Extract contiguous block
#        block_cycles = cycles[cycles.index(start):cycles.index(start) + length]
#        block = {c: seq[c] for c in block_cycles}
#
#        # Compute relative times (preserve timing gaps)
#        min_cycle = block_cycles[0]
#        shifted_block = {
#            current_time + (c - min_cycle): op for c, op in block.items()
#        }
#
#        # Add to mixed sequence
#        mixed.update(shifted_block)
#
#        # Update current_time to ensure next block starts after this one
#        current_time = max(shifted_block.keys()) + random.randint(1, 5)
#
#    return dict(sorted(mixed.items()))
#


import random

def mix_sequences(sequences, num_parts=3, seed=None, max_cycle=60):
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

