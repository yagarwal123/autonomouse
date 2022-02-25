
#include <Servo.h>
#include "TeensyTimerTool.h"
using namespace TeensyTimerTool; 

PeriodicTimer t4; 
Servo door_one;
int TTL_PIN = 33;

void door_open(Servo door) 
{ 
  door.write(90);
  delay(1000);
} 
 
void door_close(Servo door) 
{ 
  door.write(180);
  delay(1000);
} 

void callback4(const int TTL_PIN){ // saves sensor value at regular interval to pr
  if(digitalRead(TTL_PIN)==HIGH){
    Serial.print("TTL - ");
    Serial.println(millis());
  } // checking TTL pulse
}

void setup() {
  // put your setup code here, to run once:
  door_one.attach(2);
  t4.begin([=]{callback4(TTL_PIN);}, 1ms, false); 

}

void loop() {
  // put your main code here, to run repeatedly:
  t4.start();
  
  delay(5000);

  door_close(door_one);

  delay(5000);
  
  door_open(door_one);

  delay(5000);
  
  t4.stop();

}
