#include "HX711.h"
// both averaging constant and wCounter are due to calibration

float ave_reading(HX711 scale){
  float result = 0;
  for(int i=0; i<10; i++){
    result += scale.get_units();
    }
  return result/10; // returns averaged result over 10 readings
  }

float load_cell(HX711 scale) { // sliding window for weight: search for stable weight readings
  float weight = 0;
  float w1 = 0;
  int wCounter = 0;
  
  while(wCounter < 5){ // reach 5 consistent readings - can be changed
    weight = ave_reading(scale);
    w1 = ave_reading(scale);
    if(weight == w1 || weight == w1+0.1 || weight == w1-0.1){
      wCounter++;
      }else{ // if doesn't match, reset counter
        wCounter = 0;
        }
    }
  return weight;
  
  //return ave_reading(scale);
}
