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
    lickTime = -1;
    startTime = millis(); // record start time
    responseTime = startTime + RES;
    //Serial.println(startTime);
    while(millis() < responseTime){//response period
      lickCheck = read_lick(lickPin, THRESHOLD);
      //Serial.println(lickCheck);
      if ( (lickTime == -1) and (lickCheck>0) ){
        lickTime = lickCheck - startTime;
        if (lickCheck < startTime){
          //Serial.println("JNEK");
          Serial.println(lickCheck);
          Serial.println(startTime);
        }
        deliver_reward(rewardPin, liquidAmount);}
      }
      
      downTime = millis() + WAITTIME; // count 5s from now
      Serial.print("licked at ");
      Serial.println(lickTime);
      //and other communications
    }
    while(millis() < downTime){}
  }
