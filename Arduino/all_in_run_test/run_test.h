#ifndef run_test_h
#define run_test_h
#include "SdFat.h"
#include "HX711.h"
#include <Servo.h>

void run_test(Servo door_two, String ID_2, HX711 scale, int TTL_PIN, int lickPin, int rewardPin);

#endif
