#include "TeensyTimerTool.h"
using namespace TeensyTimerTool; 

void callback(int* val){ // to print out sensorValue in regular interval
  Serial.println(*val);
  }
PeriodicTimer t1; // timer to run periodic serial print
int val = 0;
int* valPt = &val;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  t1.begin([=]{callback(valPt);}, 15ms); //every 0.5ms print to serial
  t1.start();
  while (!Serial);
}

void loop() {
  // put your main code here, to run repeatedly:
  val++;
  delay(15);
}
