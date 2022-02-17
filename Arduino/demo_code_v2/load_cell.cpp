#include "HX711.h"
#include "FIR.h" //including the FIR filter functions

// both averaging constant and wCounter are due to calibration
/*
float ave_reading(HX711 scale){
  float result = 0;
  for(int i=0; i<10; i++){
    result += scale.get_units();
    }
  return result/10; // returns averaged result over 10 readings
  }
*/

float load_cell(HX711 *scale) { // sliding window for weight: search for stable weight readings
  float weight = 0;
  float aveWeight = 0;
  float w1 = 0;
  int wCounter = 0;
  float diff = 0; // difference between current reading and previous reading
  FIRFilter fir;
  FIRFilter_init(&fir); // initialise buffer
  
  while(wCounter < 2){ // reach 5 consistent readings - can be changed
    weight = scale->get_units();
    aveWeight = FIRFilter_calc(&fir, weight);
    // if(weight == w1 || weight == w1+0.1 || weight == w1-0.1)
    diff = weight - w1;
    if(diff < 0.1 && diff > -0.1){ // if the difference is within 0.1g
      wCounter++;
      }else{ // if doesn't match, reset counter
        wCounter = 0;
        }
    w1 = aveWeight; // assign new prior weight
    }
  return aveWeight;
  //return ave_reading(scale);
}
