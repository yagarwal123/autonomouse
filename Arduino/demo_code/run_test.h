#ifndef run_test_h
#define run_test_h
#include "SdFat.h"
#include "HX711.h"
#include <Servo.h>

//void run_test(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin, Servo door_one, Servo door_two);
int run_test(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin, int SCENARIO, Servo door_one, Servo door_two);

//void run_test_habituate(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin, int SCENARIO, int LED_PIN);
int run_test_habituate(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin, int SCENARIO, int LED_PIN, Servo door_one, Servo door_two);

#endif
