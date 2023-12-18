#ifndef stimulus_h
#define stimulus_h

int* start_stimulus(int *stimPin, int *oStim, int nStim, int stimProb, unsigned long stimDuration);
void stop_stimulus(int *stimPin, int nStim);

#endif