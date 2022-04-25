 #include <Servo.h>
#include <TimeLib.h>
#include "dop.h"
#include "HX711.h"
//#include "load_cell.h"
#include "clear_serial_buffer.h"
#define LOADCELL_DOUT_PIN  20
#define LOADCELL_SCK_PIN  19
#define calibration_factor 1019 //This value is obtained using the SparkFun_HX711_Calibration sketch

// define objects for door
Servo door_one;  // create servo object to control a servo
Servo door_two; // twelve servo objects can be created on most boards

// define constants for RFID
String ID;

// objects and constants for weighing
HX711 scale;
float weight;

unsigned long INTERVAL_BETWEEN_TESTS = 60*1e3;       //One minute before the same mouse is let in
unsigned long lastExitTime = 0;
String lastMouse = "";

String door1Check(){
  if (Serial1.available()){
    ID = Serial1.readStringUntil('\r');
    unsigned long recordTime = millis();
    String serOut = "";
    serOut = serOut + "Door Sensor - ID " + ID + " - Door 1 - Time " + recordTime;
    Serial.println(serOut);
  }
  else{ID = "";};
  return ID;
}

String door2Check(){
  if (Serial2.available()){
    ID = Serial2.readStringUntil('\r');
    unsigned long recordTime = millis();
    String serOut = "";
    serOut = serOut + "Door Sensor - ID " + ID + " - Door 2 - Time " + recordTime;
    Serial.println(serOut);
  }
  else{ID = "";};
  return ID;
}

void waitUntilReceive(String msg){ // waits for message from python
  while (true){
    while(!Serial.available());
    String serIn = Serial.readStringUntil('\n');
    if (serIn == msg){
      break;
    }
  }
}

void letMouseOut(String ID_2){
  clear_serial_buffer(Serial2);
  door_open(door_two);
  while (door2Check() != ID_2){} // either this or just open whenever something is in serial 2
  door_close(door_two);
  door_open(door_one);
}
  
void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  door_one.attach(2);
  door_open(door_one);
  door_two.attach(23);
  door_close(door_two);
  // door 1 open and door 2 close
  
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
    
  Serial.println("LOGGER: Starting Experiment");
}

void loop()
{
  
  // constantly checks until a known mouse appears
  // can make this an interrupt or something

  String ID_1 = door1Check();
  String ID_2 = door2Check();
  
  if ( (ID_2.length() == 0) || (ID_1.length() != 0) ){
    //scale.tare(); // reset scale again
    return;
  }

  // option: take weight here 

  Serial.println(ID_2);

  door_close(door_one);
  // option: take weight here
  //weight = load_cell(&scale);
  weight = scale.get_units();
  Serial.print("weight: ");
  Serial.print(weight);
  Serial.println("g");
  
  while(weight < 5){ // keep taking weight
  //weight = load_cell(&scale);
  weight = scale.get_units();
  Serial.print("weight: ");
  Serial.print(weight);
  Serial.println("g");
  if(Serial.available()){
    String serIn = Serial.readStringUntil('\n');
    if (serIn == "Open sesame"){
      weight = 39.99;
      }
    }
  }

  if(weight < 40){ // run test  
      
    door_open(door_two);
    lastMouse = ID_2;

    weight = scale.get_units();
    Serial.print("weight: ");
    Serial.print(weight);
    Serial.println("g");
    
    while(weight > 5){ // keep taking weight
    //weight = load_cell(&scale);
    weight = scale.get_units();
    Serial.print("weight: ");
    Serial.print(weight);
    Serial.println("g");
    if(Serial.available()){
      String serIn = Serial.readStringUntil('\n');
      if (serIn == "Manual Start"){
        weight = 0;
        }
      }
    }
    
    Serial.println("LOGGER: Closing door 2, start test");
    door_close(door_two);
    Serial.println(ID_2);
    Serial.println("Start test");

    waitUntilReceive("Stop test");
    letMouseOut(ID_2);
    lastExitTime = millis();

    Serial.println("Test complete - Start saving to file");
  }
  else{ // if weight > 40g: abolish test
    Serial.println("Invalid weight, abolish");
    door_open(door_one);
  }

  Serial.println("LOGGER: Test complete");
  clear_serial_buffer(Serial1);
  clear_serial_buffer(Serial2);
}
