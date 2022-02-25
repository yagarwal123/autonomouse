
#include <Servo.h>
#include <TimeLib.h>
#include "run_test.h"
#include "dop.h"
#include "read_id.h"
#include "check_id_exist.h"

#include "clear_serial_buffer.h"
#include "SdFat.h"
#include "time_functions.h"
#include "TeensyTimerTool.h"
#define LOADCELL_DOUT_PIN  20
#define LOADCELL_SCK_PIN  19
#define calibration_factor 1004 //This value is obtained using the SparkFun_HX711_Calibration sketch
// for SD card access--------------------------
#define SD_FAT_TYPE 3
#define SD_CONFIG SdioConfig(FIFO_SDIO)
//#define TTL_PIN 33

//using namespace TeensyTimerTool; 

//PeriodicTimer t4; // timer to run periodically check TTL pulse

time_t getTeensy3Time()
{
  return Teensy3Clock.get();
}

// define objects for door
Servo door_one;  // create servo object to control a servo
Servo door_two; // twelve servo objects can be created on most boards

// define constants for RFID
const int noMouse = 2;
String KNOWNTAGS[noMouse] = {"0007A0F7C4", "0000000000"};
String TAGNAMES[noMouse] = {"Stuart", "Little"};
String ID;

// objects and constants for weighing
HX711 scale;

SdFs sd;

// Variables for the lick and reward system
int rewardPin = 32;
int lickPin = A1;
int TTL_PIN = 33;

unsigned long INTERVAL_BETWEEN_TESTS = 60*1e3;       //One minute before the same mouse is let in
unsigned long lastExitTime = 0;
String lastMouse = "";

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
      serOut = serOut + "Door Sensor - ID " + ID + " - Door 1 - Time " + recordTime;
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
      serOut = serOut + "Door Sensor - ID " + ID + " - Door 2 - Time " + recordTime;
      Serial.println(serOut);
    }
    else {ID = "";};
  }
  return ID;
}

void letMouseOut(String ID_2){
  clear_serial_buffer(Serial2);
  door_open(door_two);
  while (door2Check() != ID_2){}
  door_close(door_two);
  door_open(door_one);
}

//void callback4(const int TTL_PIN){ // saves sensor value at regular interval to pr
//  if(digitalRead(TTL_PIN)==HIGH){
//    Serial.print("TTL - ");
//    Serial.println(millis());
//  } // checking TTL pulse
//}
  
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
  
  //Setting up the pins for the reward system
  pinMode(rewardPin, OUTPUT);
  digitalWrite(rewardPin, LOW);
    // pin for TTL pulse camera
  pinMode(TTL_PIN, INPUT);

  // time
  setSyncProvider(getTeensy3Time);

  if (timeStatus()!= timeSet) {
  Serial.println("Unable to sync with the RTC");
  return;
  }

  // initialise SD card -------------------
  // Access the built in SD card on Teensy 3.5, 3.6, 4.1 using DMA (maybe faster)
  if (!sd.begin(SD_CONFIG)) {
    sd.initErrorHalt(&Serial);
  }
  Serial.println("SD card initialized.");

  //t4.begin([=]{callback4(TTL_PIN);}, 1ms, false);
  
  while (! Serial);
  Serial.println("LOGGER: Starting Experiment");
}

void loop()
{
  // constantly checks until a known mouse appears
  // can make this an interrupt or something

  String ID_1 = door1Check();
  String ID_2 = door2Check();

  
  //TODO: dealing with rollover
  if ( (ID_2 == lastMouse) && ( (millis()-lastExitTime) < INTERVAL_BETWEEN_TESTS ) ){
    return;
  }
  
  if ( (ID_2.length() == 0) || (ID_1.length() != 0) ){
    return;
  }

  Serial.print("Check whether to start test - "); Serial.println(ID_2);
  while (true){
    while(!Serial.available());
    String serIn = Serial.readStringUntil('\n');
    if (serIn == "Do not start"){
      clear_serial_buffer(Serial1);
      clear_serial_buffer(Serial2);
      return;
    }
    else if (serIn == "Start experiment"){
      break;
    }
  }

  door_close(door_one);
  door_open(door_two);
  lastMouse = ID_2;

  //t4.start();

  // take the weight
  //Uncomment

    
  run_test(door_two, ID_2, scale, TTL_PIN, lickPin, rewardPin); // write to file during test
  letMouseOut(ID_2);
  lastExitTime = millis();

  //while (door1Check() != ID_2){}
  //door_close(door_one);
  Serial.println("Waiting for the save to complete");
  while (true){
    while(!Serial.available());
    String serIn = Serial.readStringUntil('\n');
    if (serIn == "Save complete"){
      break;
    }
  }
  Serial.println("Test complete");
  clear_serial_buffer(Serial1);
  clear_serial_buffer(Serial2);
}
