#include "run_test.h"
#include "deliver_reward.h"
#include "lick.h"
#include "TeensyTimerTool.h"
using namespace TeensyTimerTool; 

PeriodicTimer t1; // timer to run periodic serial print
PeriodicTimer t2; // timer to run periodic lick read and print

unsigned long startTime = 0;
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

void run_test(int lickPin, int THRESHOLD, int rewardPin, int liquidAmount){
  int sensorValue = 0;
  int* sensorPt = &sensorValue; // must define pointer, cannot just pass address
  
  // lambda function, pass in outerscope
  // define timers
  t1.begin([=]{callback1(sensorPt);}, 50ms, false); //every 50ms print to serial
  t2.begin([=]{callback2(lickPin, sensorPt);}, 50ms, false); // reads lickPin every 50ms
  
  for(int i=0; i<10; i++){
    Serial.print("Trial ");
    Serial.println(i);
    lickTime = -1; // time takes to lick: if not licked return -1
    lickCheck = 0; // time taken to lick from stimulus onset
    startTime = millis(); // record start time
    responseTime = startTime + RES; // acceptable responese time to stimulus
    t1.start();
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
    
    Serial.print("licked at ");
    Serial.println(lickTime);
    t1.start(); // start timer again
    
    while(millis() < downTime){ // downtime of sensor
      // other processes - communications etc
    }
    // stop timer
    t1.stop();
    t2.stop();
  }
}
