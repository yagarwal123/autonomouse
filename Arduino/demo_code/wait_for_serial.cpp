#include "Arduino.h"
#include <Servo.h>
#include "dop.h"

void waitForSerial(Servo door_one, Servo door_two){
  unsigned long startTime = millis();
  while ( (millis() - startTime)  < 1000 ){
    if (Serial.available()){return;};
  }
  door_open(door_one);
  door_open(door_two);
  while (true); //Do nothing forever

}
