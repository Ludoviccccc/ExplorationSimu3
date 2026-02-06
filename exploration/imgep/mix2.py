import random

def mix_sequences(sequences, num_parts=2, seed=None, max_cycle=60):
    """
    Randomly mixes multiple instruction programs into one.

    Args:
        sequences (list[dict]): List of programs {cycle: (type, address)}
        num_parts (int): Number of chunks to split each program into
        seed (int | None): Random seed
        max_cycle (int): Maximum cycle number in output

    Returns:
        dict: Mixed program {cycle: (type, address)}
    """

    rng = random.Random(seed)

    # Step 1: sort each program by cycle
    sorted_programs = []
    for program in sequences:
        instrs = sorted(program.items(), key=lambda x: x[0])
        sorted_programs.append(instrs)

    # Step 2: split each program into num_parts chunks
    chunks = []
    for instrs in sorted_programs:
        if not instrs:
            continue

        chunk_size = max(1, len(instrs) // num_parts)
        for i in range(0, len(instrs), chunk_size):
            chunk = instrs[i:i + chunk_size]
            chunks.append(chunk)

    # Step 3: shuffle chunks
    rng.shuffle(chunks)

    # Step 4: flatten chunks into a single instruction list
    mixed_instrs = []
    for chunk in chunks:
        mixed_instrs.extend(chunk)

    if not mixed_instrs:
        return {}

    # Step 5: assign new increasing random cycles
    num_instrs = len(mixed_instrs)
    available_cycles = sorted(
        rng.sample(range(1, max_cycle + 1), k=num_instrs)
    )

    # Step 6: build final program
    mixed_program = {
        cycle: instr
        for cycle, (_, instr) in zip(available_cycles, mixed_instrs)
    }

    return mixed_program

