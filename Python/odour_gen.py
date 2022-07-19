    # Generate odour stim according to input probability
    # or read from file

import numpy as np

def odour_gen(nChan=8, type='random', mode='test', trialNo=300):
    #nChan: number of channels
    #trialNo = number of stim arrays, default 300
    
    #type = 'random'
    #type = 'predefined'

    #mode = 'train'
    #mode = 'test'

    stimPattern = np.empty(nChan, dtype=int)

    if type == 'predefined':
        # read from file and assign to stimPattern
        pass 

    if type == 'random':
        
        if mode == 'train':
            # one target and many others
            target = 0 # user defined
            targetProb = 0.1 # user input
            prbArray = np.multiply(np.ones(nChan), (1-targetProb)/(nChan-1)) # uniform distribution for non target odours
            prbArray[target] = targetProb
            for i in range(trialNo):
                stim = np.zeros(nChan, dtype = int) # temporary storage array
                o = np.random.choice(nChan, 1, p=prbArray) # which channel to turn on
                stim[o] = 1  # make the stim array      
                stimPattern = np.vstack([stimPattern, stim])    
            #print(stim)
                
        if mode == 'test':
            # no of odours
            target = [0,5] # user define, target channelsS
            targetProb = [0.3, 0.3] # total prob = sum of 2, for any target odour, user define    
            # first determine the number of odours from probability
            prbArray = [0.1, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1] # need to be same size as nChan - max nChan odours, user input
            # index = no of odours
            for i in range(trialNo):
                stim = np.zeros(nChan, dtype = int) # temporary storage array
                nOdour = np.random.choice(nChan, 1, p=prbArray) # number of odours, p need to be 1
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
    stimPattern = odour_gen(trialNo=5)
    print(stimPattern)
