#include "run_test.h"
#include "deliver_reward.h"
#include "lick.h"

unsigned long startTime = 0;
unsigned long responseTime = 0;
unsigned long downTime = 0;
int lickTime;
unsigned long WAITTIME = 5000;
unsigned long RES = 2500;
unsigned long lickCheck = 0;

void run_test(int lickPin, int THRESHOLD, int rewardPin, int liquidAmount){
  for(int i=0; i<10; i++){
    Serial.print("Trial ");
    Serial.println(i);
    lickTime = -1; // time takes to lick: if not licked return -1
    lickCheck = 0; // time taken to lick from stimulus onset
    startTime = millis(); // record start time
    responseTime = startTime + RES; // acceptable responese time to stimulus
    //Serial.println(startTime);
    while(millis() < responseTime){// response period
      lickCheck = read_lick(lickPin, THRESHOLD);
      //Serial.println(lickCheck);
      if (lickTime == -1){
        lickCheck = read_lick(lickPin, THRESHOLD);
        if (lickCheck > 0){
          lickTime = lickCheck - startTime;
          deliver_reward(rewardPin, liquidAmount);
          }
        }
      }
      downTime = millis() + WAITTIME; // count 5s from now
    //Serial.print("Time elapsed since test start: ");
    //Serial.println(millis()- startTime);

    Serial.print("licked at ");

    //Serial.println(millis());
    Serial.println(lickTime);
      //and other communications
    //Serial.println(millis());
      
    while(millis() < downTime){}
      
    //Serial.print("Time elapsed since test start: ");
    //Serial.println(millis()- startTime);
  }
  }
