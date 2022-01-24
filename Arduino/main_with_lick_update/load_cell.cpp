#include "HX711.h"

float result;

float load_cell(HX711 scale) {
  //Serial.print("Reading: ");
  //result = scale.get_units();
  //Serial.print(result, 1); //scale.get_units() returns a float
  //Serial.print(" lbs"); //You can change this to kg but you'll need to refactor the calibration_factor
  //Serial.println();

  result = 0;
  for(int i=0; i<10; i++){
    result += scale.get_units();
    }
  return result/10; // returns averaged result over 10 readings
}
