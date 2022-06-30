#include "SdFat.h"
#include "run_test.h"
#include "deliver_reward.h"
#include "lick.h"
#include "TeensyTimerTool.h"
using namespace TeensyTimerTool; 

PeriodicTimer t1; // timer to run periodic serial print
PeriodicTimer t2; // timer to run periodic lick read and print
PeriodicTimer t3; // timer to run periodic save to file

unsigned long responseTime = 0;
unsigned long downTime = 0;
int lickTime;
unsigned long WAITTIME = 5000;
unsigned long RES = 2500;
int lickCheck = 0;

void callback1(int *sensorAddr){ // to print out sensorValue in regular interval
  //Serial.print("display: ");
  Serial.println(*sensorAddr);
  }

void callback2(int lickPin, int* sensorAddr) // reads sensor value 
{
  *sensorAddr = analogRead(lickPin);
  //Serial.println(*sensorAddr);
  //Serial.println("r");
  }

void callback3(int* sensorAddr, unsigned long* timePt, FsFile* pr){ // saves sensor value at regular interval to pr
  pr->print(millis() - *timePt);
  pr->print(", ");
  pr->println(*sensorAddr);
  }

void run_test(int lickPin, int THRESHOLD, int rewardPin, int liquidAmount, FsFile* pr){
  int sensorValue = 0;
  int* sensorPt = &sensorValue; // must define pointer, cannot just pass address
  unsigned long startTime = 0;
  unsigned long* timePt = &startTime; // pointer to start time of test
  
  // lambda function, pass in outerscope
  // define timers
  t1.begin([=]{callback1(sensorPt);}, 100ms, false); //every 100ms print to serial
  t2.begin([=]{callback2(lickPin, sensorPt);}, 15ms, false); // reads lickPin every 50ms
  t3.begin([=]{callback3(sensorPt, timePt, pr);}, 1ms); // saves amplitude every 1ms
  
  for(int i=1; i<11; i++){
    //Serial.print("Trial ");
    //Serial.println(i);
    lickTime = -1; // time takes to lick: if not licked return -1
    lickCheck = 0; // time taken to lick from stimulus onset
    startTime = millis(); // record start time
    responseTime = startTime + RES; // acceptable responese time to stimulus
    t1.start(); // start 
    //t3.start(); // start saving to file
    //Serial.println(startTime);
    while(millis() < responseTime){// response period
      if (lickTime == -1){ // if mouse hasn't responded
        lickCheck = read_lick(lickPin, THRESHOLD, &sensorValue); // read_lick returns time licked
        if (lickCheck > 0){
          t2.start(); // start reading at longer intervals if mouse has licked
          lickTime = lickCheck - startTime;
          deliver_reward(rewardPin, liquidAmount);// if mouse has licked during response period
          }
        }
      }
      downTime = millis() + WAITTIME; // count 5s from now

    t1.stop();// stop timers whether or not there was licking
    if (lickTime < 0){ // start reading at longer intervals if mouse hasnt licked
      t2.start();
    }
    
    Serial.print("Trial ");
    Serial.println(i);
    Serial.print("lick sensor ");
    Serial.println(lickTime);
    t1.start(); // start timer again
    
    while(millis() < downTime){ // downtime of sensor
      // other processes - communications etc
    }
    // stop timers
    t1.stop();
    t2.stop();
    //t3.stop();
  }
  t3.stop();
}