
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


void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  door_one.attach(2);
  door_close(door_one);
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

void loop()
{
  Serial.println("starting round");
  door_close(door_one); // for demo purpose, to be deleted

  // door 1 open and door 2 close
  //door_open(door_one);
  door_close(door_two);

  // constantly checks until a known mouse appears
  // can make this an interrupt or something
  
  // check antenna 1
  ID = read_id(Serial1);
  while (ID.length() != 10) {
    ID = read_id(Serial1);
    //delay(150); // a delay is needed here to read, >150??? no need of delay here
  }
  Serial.println(ID);
  String mouseName = check_id_exist(ID, KNOWNTAGS, TAGNAMES, noMouse);
  Serial.println(mouseName);
  if (mouseName != "Mouse does not exist") {
    door_open(door_one); // if mouse exists in database, open the door
  }
  
  // clear buffer has no use here
  //clear_serial_buffer(Serial1);
 
    // checks second antenna and see if tag exists
  ID_sf = read_id_sf(Serial2);
  while(ID_sf.length() != 12){
    ID_sf = read_id_sf(Serial2); // case of no tag or unknown tag present
  }
  // if tag is recognised
  Serial.println(ID_sf);
  // clear buffer for antenna 1
  clear_serial_buffer(Serial1);

  // TODO: if needed: wait for buffer to fill up if mouse 2 present
  // then read buffer to see if mouse 2 present

  // close first door
  door_close(door_one);

  // open second door
  Serial.println("opening door 2");
  door_open(door_two);

  // record mouse entrace
  Serial.print("Entering: ");
  Serial.println(ID);
  Serial.println(now());

  // take the weight
  weight = load_cell(scale);
  Serial.print(mouseName);
  Serial.print(" weights: ");
  Serial.print(weight);
  Serial.println("g");
/*
  // optional: if weight is >0 and < 40, close door 2
  while(weight < 15 || weight > 40){
    weight = load_cell(scale);
  }

  // when the scale indicates mouse is on platform
  // close door 2 and start test
*/
  delay(5000);
  Serial.println("closing door 2");
  door_close(door_two);

  int liquidAmount = 500; // command from raspi
  run_test(lickPin, THRESHOLD, rewardPin, liquidAmount);
   
   // clear buffer for antenna 1
  clear_serial_buffer(Serial1);
}
