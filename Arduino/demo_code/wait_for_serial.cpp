  /*****************************************************************************
  Function to detect when python is crashing
  Assume python will not send anything through serial if it has crashed
  *****************************************************************************/

#include "Arduino.h"
#include <Servo.h>
#include "dop.h"

void waitForSerial(Servo door_one, Servo door_two){
  unsigned long startTime = millis();
  while ( (millis() - startTime)  < 30000 ){
    if (Serial.available()){return;};
  }
  Serial.println("no response from python for 30s, opening all doors");
  door_open(door_one,1);
  door_open(door_two,2);
  //pre 20230719
  //door_open(door_one);
  //door_open(door_two);
  while (true); //Do nothing forever

}
