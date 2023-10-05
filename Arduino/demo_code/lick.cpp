  /*****************************************************************************
  Detection code for lick sensor, calibrated to the lick of a lab mouse
  *****************************************************************************/
  
#include <Arduino.h>
#include "lick.h"
//#include "TeensyTimerTool.h"
//using namespace TeensyTimerTool; 

unsigned long millisec = 0;
unsigned long finalTime = 0;
unsigned long read_lick(int sensorPin, int THRESHOLD, int *sensorAddr) {
  //int sensorValue = 0;
  finalTime = 0;
  
  // read the value from the sensor:
  *sensorAddr = analogRead(sensorPin); // read sensor data and print
  //Serial.println(*sensorAddr);
  
  if (*sensorAddr > THRESHOLD) {
    Serial.println(*sensorAddr);
    int tAbove = 1;
    millisec = millis();
    while (*sensorAddr > THRESHOLD){
      *sensorAddr = analogRead(sensorPin);
      //Serial.println(sensorValue);
      tAbove = tAbove+1;
    }
    if (tAbove > 50) {// TODO: UP time due to calibration
      finalTime = millisec;
      //Serial.println("Lick");
      //Serial.println(sensorValue);
    }
  } 

  // stop timer before exiting function
  //t2.stop();
  
  return finalTime;
}
