/* Sweep
 by BARRAGAN <http://barraganstudio.com> 
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://arduino.cc/en/Tutorial/Sweep
*/ 

#include <Arduino.h>
#include <Servo.h> 
#include "dop.h"
 
//Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
 
void door_open(Servo door) // might need to decrease speed
{ 
  door.write(90);
  delay(1000); // why have delay here?
} 
 
void door_close(Servo door) 
{ 
  door.write(180);
  delay(1000);
} 
