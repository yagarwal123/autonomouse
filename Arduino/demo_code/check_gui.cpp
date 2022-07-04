#include "Arduino.h"
#include <Servo.h>
#include "dop.h"

//Note: There will be times where python is suuposed to be busy and not reading. For eg when stopping rasp recording, reading raw data etc.
// So we need to be careful about where we put the check_gui function
void check_gui(Servo door_one, Servo door_two){
  if (Serial.available()){return;}; //This means something is coming from the GUI (in the buffer currently, so GUI is working)
  Serial.println("Check GUI");
  //TODO: timeout
  Serial.setTimeout(500); //Reduce time waiting, check if it is required
  String serIn = Serial.readStringUntil('\n');
  Serial.setTimeout(1000);  //Set back to default, delete if timeout is not being reduced
  if (serIn != "Working"){
    door_open(door_one);
    door_open(door_two);
    while (true); //Do nothing forever
  }


}
