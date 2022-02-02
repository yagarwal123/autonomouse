
#include <Servo.h>
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

unsigned long timeDoor1;
unsigned long timeDoor2;
String door1ID = "";
String door2ID = "";
boolean mouseAtDoorOne = false;
boolean mouseAtDoorTwo = false;


void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  door_one.attach(2);
  door_open(door_one);
  door_two.attach(23);
  door_close(door_two);
  /*
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
    scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
  */
  //Setting up the pins for the reward system
  pinMode(rewardPin, OUTPUT);
  digitalWrite(rewardPin, LOW);
}
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
      String serOut = "Door Sensor - ID" + ID + "Door 1 - Time " + recordTime;
      Serial.println(serOut);
    }
    else {ID = "";};
  }
  return ID;
}

boolean door2Check(){
    // checks second antenna and see if tag exists
  ID_sf = read_id_sf(Serial2);
  if(ID_sf.length() == 12){
    Serial.println(ID_sf); // if tag is recognised
    mouseAtDoorTwo = true;
  }
  else {mouseAtDoorTwo = false;};
  return mouseAtDoorTwo; 
}
  
void loop()
{
  mouseAtDoorOne = door1Check();
  // constantly checks until a known mouse appears
  // can make this an interrupt or something
  //Serial.println("aa");

  //Serial.println(mouseAtDoorOne);
  // clear buffer has no use here
  //clear_serial_buffer(Serial1);
 
    // checks second antenna and see if tag exists
  //mouseAtDoorTwo = door2Check();

  // TODO: if needed: wait for buffer to fill up if mouse 2 present
  // then read buffer to see if mouse 2 present

  

  // take the weight
//  weight = load_cell(scale);
//  Serial.print(" weights: ");
//  Serial.print(weight);
//  Serial.println("g");
//
//  //delay(5000);
//  Serial.println("closing door 2");
//  door_close(door_two);
//
//  int liquidAmount = 500; // command from raspi
//  run_test(lickPin, THRESHOLD, rewardPin, liquidAmount);
  
}
