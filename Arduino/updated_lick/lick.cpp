//#include <Arduino.h>
//#include "lick.h"
//int lickno = 0;  
//void read_lick(int sensorPin, int THRESHOLD) {
//  // read the value from the sensor:
//  int sensorValue = analogRead(sensorPin); 
//  if (sensorValue > THRESHOLD) {
//    int t_above = 1;
//    sensorValue = analogRead(sensorPin);
//    if (sensorValue > THRESHOLD) {t_above = t_above + 1;}
//    if (t_above > 10) {
//      Serial.println("Lick");
//      Serial.println(sensorValue);
//      lickno = lickno+1;
//      Serial.print("Lick no = "); Serial.println(lickno);
//      int t_below = 0;
//      while (t_below < 100) {
//         sensorValue = analogRead(sensorPin);
//         //Serial.println(sensorValue);
//         if (sensorValue < THRESHOLD) {t_below = t_below + 1;}
//         else {t_below = 0;}
//         sensorValue = analogRead(sensorPin);
//         //if (t_below>0){Serial.println(t_below);}        
//      }
//      Serial.print("Lick no = "); Serial.println(lickno); 
//      Serial.println("lick out");
//      t_above = 0;
//    }
//  } 
//
//}


#include <Arduino.h>
#include "lick.h"
#include "TeensyTimerTool.h"
using namespace TeensyTimerTool; 

unsigned long millisec = 0;
unsigned long finalTime = 0;

PeriodicTimer t2; // timer to run periodic lick read

void callback(int sensorValue){
  // to print out sensorValue in regular interval
  Serial.println(sensorValue);
  }

unsigned long read_lick(int sensorPin, int THRESHOLD) {
  int sensorValue = 0;
  finalTime = 0;
  
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin); // read sensor data and print
  Serial.println(sensorValue);
  
  // define timer, this callback function only runs during a lick
  t2.begin([=]{callback(sensorValue);}, 1ms); // reads lickPin every 50ms and print to serial
  
  if (sensorValue > THRESHOLD) {
    int tAbove = 1;
    millisec = millis();
    while (sensorValue > THRESHOLD){
      sensorValue = analogRead(sensorPin);
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
  t2.stop();
  
  return finalTime;
}
