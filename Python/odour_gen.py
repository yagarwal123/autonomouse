    # Generate odour stim according to input probability
    # or read from file

import numpy as np

def odour_gen(target, targetProb, nPrbArray, nChan=8, trialNo=300):
    #nChan: number of channels
    #trialNo = number of stim arrays, default 300
    
    #type = 'random'
    #type = 'predefined'
    
    # need user to input: target(s), target(s)Prob, nPrbArray = probability array for the number of odours to present

    stimPattern = np.empty(nChan, dtype=int)
                
    # first determine the number of odours from probability
    for i in range(trialNo):
        stim = np.zeros(nChan, dtype = int) # temporary storage array
        nOdour = np.random.choice(nChan, 1, p=nPrbArray) # number of odours, p need to be 1
        nOdour += 1
        #print(nOdour)

        # generate stim array
        prbArray = np.multiply(np.ones(nChan), (1-sum(targetProb))/(nChan-len(target)))
        prbArray[target] = targetProb
        o = np.random.choice(nChan, nOdour, replace=False, p=prbArray) # which channels to turn on
        stim[o] = 1  # make the stim array       
        stimPattern = np.vstack([stimPattern, stim])     
        #print(stim)

    # maybe option to save randomly generated pattern to file
    return np.delete(stimPattern, 0, axis=0) # remove first line from np.empty

if __name__=='__main__':
    # for training mode:
    # target = 0 
    # targetProb = 0.1
    target = [0] # user define, target channels, can have multiple targets
    targetProb = [0.3] # total prob = sum of 2, for any target odour, user define   
    nPrbArray = [0.1, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1] # need to be same size as nChan - max nChan odours, user input
    nPrbArray = [0, 1, 0, 0, 0, 0, 0, 0]
    stimPattern = odour_gen(target, targetProb, nPrbArray, nChan=8, trialNo=5)
    print(stimPattern)
