#include "HX711.h"
#include "load_cell.h"
#define LOADCELL_DOUT_PIN  4
#define LOADCELL_SCK_PIN  5
#define calibration_factor 457 //This value is obtained using the SparkFun_HX711_Calibration sketch

HX711 scale;
float weight;

void setup() {
  // put your setup code here, to run once:
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

}

void loop() {
  // put your main code here, to run repeatedly:
  //weight = load_cell(scale);
  weight = scale.get_units();
  Serial.println(weight,1);
  //Serial.println("g");
}
