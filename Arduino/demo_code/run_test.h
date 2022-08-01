#ifndef run_test_h
#define run_test_h
#include "SdFat.h"
#include "HX711.h"

void run_test(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, HX711 *scale, int pumpPin);

#endif
