import os

NUM_RUNS = 5

if __name__=='__main__':
    ###############################
    ## LOG
    ###############################
    filepath_log = os.path.join('runs', 'RUN_DIR', 'log.txt')
    
    with open(filepath_log) as fin:
        lines = [l.rstrip() for l in fin.readlines()]
        
    logs_per_runs = [ [] for _ in range(NUM_RUNS) ]
    
    RUN = 0
    CURSOR = -1
    for l in lines:
        
        ## head
        if l == f'Run {RUN:02d}: ======================':
            CURSOR += 1
            RUN += 1
        
        ## body
        if CURSOR > -1:
            logs_per_runs[CURSOR].append(l)
            
    
    beststep_per_runs = []
    for logs in logs_per_runs:
        
        beststep = 0
        bestscore = 0.
        
        for l in logs:
            if l[:4] == 'Step': # l = 'Step: 01,\tScore: 0.3125554'
                l = l.split(',\t')  # l = ['Step: 01', 'Score: 0.3125554']
                
                step = l[0] # step = 'Step: 01'
                step = step.split(' ') # step = ['Step:', '01']
                step = int(step[1])
                
                score = l[1] # score = 'Score: 0.3125554'
                score = score.split(' ') # score = ['Score:', '0.3125554']
                score = float(score[1])
                
                if score > bestscore:
                    bestscore = score
                    beststep = step
                    
        beststep_per_runs.append((beststep, bestscore))
        
    for i, (st, sc) in enumerate(beststep_per_runs):
        print(i, st, sc)
        
        
    ###############################
    ## MOLS
    ###############################
    bestmols = []
    for RUN, (st, sc) in enumerate(beststep_per_runs):
        
        filepath_mols = os.path.join('runs', 'RUN_DIR', f'run_{RUN:02d}', 'mols.txt')
        
        with open(filepath_mols) as fin:
            lines = [l.rstrip() for l in fin.readlines()]
        
        CURSOR = 0
        while CURSOR < len(lines) and lines[CURSOR] != f'molecules obtained at step {st}':
            CURSOR += 1
        
        mols = []
        if lines[CURSOR] == f'molecules obtained at step {st}':
            CURSOR += 2 # to skip the header 'score	gsk3b	jnk3	qed	sa	smiles'
            while CURSOR < len(lines) and lines[CURSOR] != f'molecules obtained at step {st+1}':
                smi = lines[CURSOR].split('\t')[-1]
                mols.append(smi)
                CURSOR += 1
                
        print(RUN, len(mols))
        bestmols.extend(mols)
                
    print(len(bestmols))
    
    ###############################
    ## SAVE
    ###############################
    with open(os.path.join('runs', 'MARS.txt'), 'w') as fout:
        for smi in bestmols:
            fout.write(f'{smi}\n')