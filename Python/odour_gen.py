    # Generate odour stim according to input probability
    # or read from file

import numpy as np

def odour_gen2(prbArray, nPrbArray, nChan, trialNo=1):
    # each odour channel has its own corresponding blank channel
    # used for the current olfactometer

    #nChan: number of channels
    #trialNo = number of stim arrays, default 300
    
    # need user to input: target(s), target(s)Prob, nPrbArray = probability array for the number of odours to present

    stimPattern = np.empty(nChan*2, dtype=int)
                
    # first determine the number of odours from probability
    for i in range(trialNo):
        stim = np.zeros(nChan*2, dtype = int) # temporary storage array
        nOdour = np.random.choice(nChan, 1, p=nPrbArray) # number of odours, p need to be 1
        nOdour += 1
        # print(nOdour[0])

        # generate stim array
        # prbArray = np.multiply(np.ones(nChan), (1-sum(targetProb))/(nChan-len(target)))
        # prbArray[target] = targetProb
        o = np.random.choice(nChan, nOdour, replace=False, p=prbArray) # which channels to turn on, p=probability of each element being selected
        stim[o] = 1  # make the stim array       
         # make the blank array
        for j in range(nChan): 
            if stim[j] == 0: stim[nChan+j] = 1
        stimPattern = np.vstack([stimPattern, stim])     
        #print(stim)
    
    return np.delete(stimPattern, 0, axis=0) # remove first line from np.empty


if __name__=='__main__':
    # for training mode:
    # target = 0 
    # targetProb = 0.1
    target = [0] # user define, target channels, can have multiple targets
    prbArray = [0.1, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1] # need to be same size as nChan - max nChan odours, user input
    nPrbArray = [0.9, 0.1, 0, 0, 0, 0, 0, 0]
    stimPattern = odour_gen2(prbArray, nPrbArray, nChan=8, trialNo=5)
    print(stimPattern)

"""
def odour_gen(prbArray, nPrbArray, nChan, trialNo=1):
    # for 15 channels: first 8 odours lst 7 blanks
    # not used anymore for the current olfactometer
    #nChan: number of channels
    #trialNo = number of stim arrays, default 300
    
    # need user to input: target(s), target(s)Prob, nPrbArray = probability array for the number of odours to present

    stimPattern = np.empty(nChan*2-1, dtype=int)
                
    # first determine the number of odours from probability
    for i in range(trialNo):
        stim = np.zeros(nChan*2-1, dtype = int) # temporary storage array
        nOdour = np.random.choice(nChan, 1, p=nPrbArray) # number of odours, p need to be 1
        nOdour += 1
        # print(nOdour[0])

        # generate stim array
        # prbArray = np.multiply(np.ones(nChan), (1-sum(targetProb))/(nChan-len(target)))
        # prbArray[target] = targetProb
        o = np.random.choice(nChan, nOdour, replace=False, p=prbArray) # which channels to turn on, p=probability of each element being selected
        stim[o] = 1  # make the stim array       
         # make the blank array
        for j in range(nChan-nOdour[0]): # 1 less blank than odour and correct for 0 index in python
            stim[nChan+j] = 1
        stimPattern = np.vstack([stimPattern, stim])     
        #print(stim)
    
    return np.delete(stimPattern, 0, axis=0) # remove first line from np.empty

"""    