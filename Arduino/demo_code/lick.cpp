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

unsigned long millisec = 0;
unsigned long finalTime = 0;
unsigned long read_lick(int sensorPin, int THRESHOLD) {
  finalTime = 0;
  // read the value from the sensor:
  int sensorValue = analogRead(sensorPin); 
  if (sensorValue > THRESHOLD) {
    int tAbove = 1;
    millisec = millis();
    while (sensorValue > THRESHOLD){
      sensorValue = analogRead(sensorPin);
      tAbove = tAbove+1;
    }
    if (tAbove > 50) {// TODO: UP time due to calibration
      finalTime = millisec;
      //Serial.println("Lick");
      //Serial.println(sensorValue);
    }
  } 
  return finalTime;
}
