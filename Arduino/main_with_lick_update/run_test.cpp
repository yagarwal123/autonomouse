#include "run_test.h"
#include "deliver_reward.h"
//#include "lick.h"
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
unsigned long millisec = 0;
int tAbove;


void callback1(int sensorValue){
  // to print out sensorValue in regular interval
  Serial.println(sensorValue);
  }


void callback2(int lickPin, int sensorValue) // reads sensor value and print to serial
{
  sensorValue = analogRead(lickPin);
  Serial.println(sensorValue);
  }

void run_test(int lickPin, int THRESHOLD, int rewardPin, int liquidAmount){
  int sensorValue = 0;
  
  // lambda function, pass in outerscope
  // define timers
  t1.begin([=]{callback1(sensorValue);}, 100ms, false); // reads lickPin every 50ms and print to serial
  t2.begin([=]{callback2(lickPin, sensorValue);}, 100ms, false); // reads lickPin every 50ms and print to serial
  
  for(int i=0; i<10; i++){
    Serial.print("Trial ");
    Serial.println(i);
    lickTime = -1; // time takes to lick: if not licked return -1
    //lickCheck = 0; // time taken to lick from stimulus onset
    startTime = millis(); // record start time
    responseTime = startTime + RES; // acceptable responese time to stimulus
    //Serial.println(startTime);
    while(millis() < responseTime){// response period
      if (lickTime == -1){ // if mouse hasn't responded
        //lickCheck = read_lick(lickPin, THRESHOLD); // read_lick returns time licked

        t1.start();
        // read the value from the sensor:
        sensorValue = analogRead(lickPin); // read sensor data and print
        //Serial.println(sensorValue);
        
        if (sensorValue > THRESHOLD) { // if amplitude crosses threshold
          tAbove = 1;
          millisec = millis();
          while (sensorValue > THRESHOLD){ // remain in the loop as long as amplitude is above threshold
            sensorValue = analogRead(lickPin);
            //Serial.println(sensorValue);
            tAbove = tAbove+1;
            }
          if (tAbove > 50) {// TODO: UP time due to calibration
            lickTime = millisec - startTime;
            }
          }
           
        if (lickTime > 0){
          deliver_reward(rewardPin, liquidAmount);// if mouse has licked during response period
          t1.stop();
          }
        
        }else{ // if mouse has already responded
          t2.start();
        }
      }
      downTime = millis() + WAITTIME; // count 5s from now
    t2.stop();// stop timer
    
    //Serial.print("licked at ");
    //Serial.println(lickTime);

    // start periodic timer
    t2.start();
    while(millis() < downTime){
     
    }
    // stop timer
    t2.stop();
    
      // other communication if needed
  }
}
