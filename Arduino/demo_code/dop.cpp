/* Sweep
Door control

adopted from:
 by BARRAGAN <http://barraganstudio.com> 
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://arduino.cc/en/Tutorial/Sweep
*/ 


#include <Arduino.h>
#include <Servo.h> 
#include "dop.h"

int angle_close;
int angle_open;
 
//Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
 
void door_open(Servo door, int servonumber) // might need to decrease speed
// 20230719 added second input argument to indicate what should be the correct 'open' angle for door 1 and 2
{ 
  //int cur_angle = door.read(); 
  
  if (servonumber == 1){
    angle_close = 45;//20230720
    //angle_close = 30
    angle_open = 115;
  }
  if (servonumber == 2){
    angle_close = 45;
    angle_open = 109;
  }
  //int angle_close = 30;
  //int angle_open = 115;

  Serial.print("angle_close:");  
  Serial.print(angle_close);  
  Serial.print("angle_open:");  
  Serial.print(angle_open);  

  Serial.print("door: ");  
  Serial.print(servonumber);       
  Serial.print("open: pre: ");  
  Serial.print(door.read());       
  for(int pos = angle_close; pos <= angle_open; pos += 1) // goes from 180 degrees to 90 degrees 
  {                                  // in steps of 1 degree 
    door.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(3);                       // adjust for speed
  }
  Serial.print(" post: ");  
  Serial.println(door.read());  
  
} 
 
void door_close(Servo door, bool slower) 
{ 
  for(int pos = 115; pos >= 45; pos -= 1) // goes from 180 degrees to 90 degrees 
  {                                  // in steps of 1 degree 
    door.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(3);                       // adjust for speed
    if (slower){
      delay(6); // decrease door speed on closing
    }
  }
} 



// pre 20230719
//void door_open(Servo door) // might need to decrease speed
//{ 
//  //door.write(90);
//  //delay(1000); // why have delay here?
//  for(int pos = 45; pos <= 115; pos += 1) // goes from 180 degrees to 90 degrees 
//  {                                  // in steps of 1 degree 
//    door.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(3);                       // adjust for speed
//  }
//} 
// 
//void door_close(Servo door, bool slower) 
//{ 
//  //door.write(180);
//  //delay(1000);
//  for(int pos = 115; pos >= 45; pos -= 1) // goes from 180 degrees to 90 degrees 
//  {                                  // in steps of 1 degree 
//    door.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(3);                       // adjust for speed
//    if (slower){
//      delay(6); // decrease door speed on closing
//    }
//  }
//} 