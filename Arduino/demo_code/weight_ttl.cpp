#include "weight_ttl.h"
#include "load_cell.h"
#include "HX711.h"
#include "TeensyTimerTool.h"
using namespace TeensyTimerTool; 

PeriodicTimer t0(TMR4); // timer to run periodic serial print

void callback0(const int TTL_PIN){ // saves sensor value at regular interval to pr
  if(digitalRead(TTL_PIN)==HIGH){
    Serial.print("TTL - ");
    Serial.println(millis());
  } // checking TTL pulse
}
  

float weight_ttl(HX711 *scale, const int TTL_PIN){
  t0.begin([=]{callback0(TTL_PIN);}, 1ms);
  float w = load_cell(scale);
  //Comment out
  //Serial.println("Enter mouse weight:");
  //while(!Serial.available()){}
  //weight = Serial.parseFloat();

  // optional: if weight is >0 and < 40, close door 2
  while(w < 15){ // keep taking weight
    w = load_cell(scale);
    //Serial.println("Enter mouse weight:");
    //while(!Serial.available()){}
    //weight = 20;
    Serial.print("weight: ");
    Serial.print(w);
    Serial.println("g");
  }
  t0.stop();
  return w;
}
