
#include <Servo.h>
#include <TimeLib.h>
#include "run_test.h"
#include "dop.h"
#include "read_id.h"
#include "check_id_exist.h"
#include "HX711.h"
#include "load_cell.h"
#include "read_id_sf.h" // include sparkfun decoder temporarily for testing
#include "clear_serial_buffer.h"
#define LOADCELL_DOUT_PIN  4
#define LOADCELL_SCK_PIN  5
#define calibration_factor 430.5 //This value is obtained using the SparkFun_HX711_Calibration sketch


// define objects for door
Servo door_one;  // create servo object to control a servo
Servo door_two; // twelve servo objects can be created on most boards

// define constants for RFID
const int noMouse = 2;
String KNOWNTAGS[noMouse] = {"0007A0F7C4", "0000000000"};
String TAGNAMES[noMouse] = {"Stuart", "Little"};
String ID, ID_sf;

// objects and constants for weighing
HX711 scale;
float weight;

// Variables for the lick and reward system
int rewardPin = 32;
int lickPin = A13;
int THRESHOLD = 1000;

String door1Check(){
  ID = read_id(Serial1);
  if (ID.length() != 10) {
    ID = "";
  }
  else{
    unsigned long recordTime = millis();
    //Serial.println(ID);
    String mouseName = check_id_exist(ID, KNOWNTAGS, TAGNAMES, noMouse);
    //Serial.println(mouseName);
    if (mouseName != "Mouse does not exist") {
      String serOut = "";
      serOut = serOut + "Door Sensor - ID" + ID + "Door 1 - Time " + recordTime;
      Serial.println(serOut);
    }
    else {ID = "";};
  }
  return ID;
}

String door2Check(){
  ID = read_id(Serial2);
  if (ID.length() != 10) {
    ID = "";
  }
  else{
    unsigned long recordTime = millis();
    String mouseName = check_id_exist(ID, KNOWNTAGS, TAGNAMES, noMouse);
    if (mouseName != "Mouse does not exist") {
      String serOut = "";
      serOut = serOut + "Door Sensor - ID" + ID + "Door 2 - Time " + recordTime;
      Serial.println(serOut);
    }
    else {ID = "";};
  }
  return ID;
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
  /*
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
    scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
  */
  //Setting up the pins for the reward system
  pinMode(rewardPin, OUTPUT);
  digitalWrite(rewardPin, LOW);

  // set time
  //setTime(12,44,1,6,1,2022);
}

void loop()
{
  // constantly checks until a known mouse appears
  // can make this an interrupt or something

  String ID_1 = door1Check();
  String ID_2 = door2Check();
  
  if ( (ID_2.length() == 0) || (ID_1.length() != 0) ){
    return;
  }
  door_close(door_one);
  door_open(door_two);

  // take the weight
  //Uncomment
  //weight = load_cell(scale);
  //Comment out
  Serial.println("Enter mouse weight:");
  while(!Serial.available()){}
  weight = Serial.parseFloat();

  // optional: if weight is >0 and < 40, close door 2
  while(weight < 15){ // keep taking weight
    //weight = load_cell(scale);
    Serial.println("Enter mouse weight:");
    while(!Serial.available()){}
    weight = Serial.parseFloat();
    Serial.print("weight: ");
    Serial.print(weight);
    Serial.println("g");
  }

  if(weight < 40){ // run test
    String serOut = "";
    serOut = serOut + "Weight Sensor - Weight " + weight + "g - Time " + millis();
    Serial.println(serOut);
    Serial.println("closing door 2, start test");
    door_close(door_two);
  
    int liquidAmount = 200; // command from raspi
    run_test(lickPin, THRESHOLD, rewardPin, liquidAmount);
    Serial.println("Test complete - Start saving to file");
  }
  else{
    Serial.println("Invalid weight, abolish");
  }
  clear_serial_buffer(Serial2);
  door_open(door_two);
  while (door2Check() == ID_2){}
  door_close(door_two);
  
  clear_serial_buffer(Serial1);
  door_open(door_one);
  while (door1Check() == ID_2){}
  door_close(door_one);
  while (true){
    while(!Serial.available()){}
    String serIn = Serial.readString();
    if (serIn == "Save complete"){
      break;
    }
  }
  door_open(door_one);
}
