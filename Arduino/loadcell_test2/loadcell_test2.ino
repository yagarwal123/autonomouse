#include "FIR.h" //including the FIR filter functions
#include "HX711.h"
#define LOADCELL_DOUT_PIN  20
#define LOADCELL_SCK_PIN  19
#define calibration_factor 1004 //This value is obtained using the SparkFun_HX711_Calibration sketch

HX711 scale;
//Declaring the filter struct variable
FIRFilter fir;

void setup() {
  // put your setup code here, to run once:
  //Initialise the filter coefficient (the weight)
  FIRFilter_init(&fir);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  //Calculating the filtered values
  int weight = scale.get_units();
  FIRFilter_calc(&fir, scale.get_units());
  Serial.println(weight,1);

}
