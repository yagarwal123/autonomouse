
#include <Servo.h>
#include <TimeLib.h>
#include "run_test.h"
#include "dop.h"
#include "read_id.h"
#include "check_id_exist.h"
#include "HX711.h"
#include "load_cell.h"
#include "clear_serial_buffer.h"
#include "SdFat.h"
#include "time_functions.h"
//#include "TeensyTimerTool.h"
#define LOADCELL_DOUT_PIN  20
#define LOADCELL_SCK_PIN  19
#define calibration_factor 1004 //This value is obtained using the SparkFun_HX711_Calibration sketch
// for SD card access--------------------------
#define SD_FAT_TYPE 3
#define SD_CONFIG SdioConfig(FIFO_SDIO)
//#define TTL_PIN 33

SdFs sd;
FsFile file;

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
float weight;

// Variables for the lick and reward system
int rewardPin = 32;
int lickPin = A1;
const int TTL_PIN = 33;

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

void waitUntilReceive(String msg){
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
  while (door2Check() != ID_2){}
  door_close(door_two);
  door_open(door_one);
}

void callback4(){ // saves sensor value at regular interval to pr
    Serial.print("TTL - "); Serial.println(millis());
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
  
  //Setting up the pins for the reward system
  pinMode(rewardPin, OUTPUT);
  digitalWrite(rewardPin, LOW);
    // pin for TTL pulse camera
  pinMode(TTL_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(TTL_PIN), callback4, RISING);

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
  Serial.println("LOGGER: SD card initialized.");

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

  // take the weight
  //Uncomment
  weight = load_cell(&scale);
  //Comment out
  //Serial.println("Enter mouse weight:");
  //while(!Serial.available()){}
  //weight = Serial.parseFloat();

  // optional: if weight is >0 and < 40, close door 2
  while(weight < 15){ // keep taking weight
    weight = load_cell(&scale);
    //Serial.println("Enter mouse weight:");
    //while(!Serial.available()){}
    //weight = 20;
    Serial.print("weight: ");
    Serial.print(weight);
    Serial.println("g");
  }

  if(weight < 40){ // run test
    String serOut = "";
    serOut = serOut + "Weight Sensor - Weight " + weight + "g - Time " + millis();
    Serial.println(serOut);
    Serial.println("LOGGER: Closing door 2, start test");
    door_close(door_two);
    //t4.start();

    // create file
    String fileName = ID_2 + month()+"_"+day()+"_"+hour()+"_"+minute()+"_"+second()+".txt";
    Serial.print("LOGGER: Filename - ");Serial.println(fileName);
    char buf[30];
    fileName.toCharArray(buf, 30);
    // Remove old version to set create time.
    if (sd.exists(fileName)) {
      Serial.println("Duplicate file!!!");
    }

    if (!file.open(buf, FILE_WRITE)) { // filename needs to be in char
      Serial.println(F("file.open failed"));
      // TODO: mission abort;
    }
    
    // Print current date time to file.
    file.print(F("Test file at: "));
    printNow(&file);
    file.println();
    file.print(F("time(ms), ")); // print headings
    file.println(F("amplitude"));
    
    Serial.print("Send parameters: Incoming mouse ID - "); Serial.println(ID_2);
    while (!Serial.available());
    int THRESHOLD = Serial.readStringUntil('\n').toInt();
    while (!Serial.available());
    int liquidAmount = Serial.readStringUntil('\n').toInt();
    while (!Serial.available());
    int WAITTIME = Serial.readStringUntil('\n').toInt();

    Serial.print("LOGGER: Received - Liquid Amount - ");Serial.println(liquidAmount);
    Serial.print("LOGGER: Received - Lick Threhold - ");Serial.println(THRESHOLD);
    Serial.print("LOGGER: Received - Inter trial interval - ");Serial.println(WAITTIME);
    
    run_test(lickPin, THRESHOLD, rewardPin, liquidAmount, &file, WAITTIME); // write to file during test
    file.close(); // close the file
    letMouseOut(ID_2);
    lastExitTime = millis();

    
    //t4.stop(); // stop reading TTL pulse
    // TODO: send file to PC through Serial
    //file.rewind();
    Serial.println("Stop recording");

    while (true){
      while(!Serial.available());
      String serIn = Serial.readStringUntil('\n');
      if (serIn == "Camera closed"){
        break;
      }
    }
    
    Serial.println("Sending raw data");

    // open file again
    if (!file.open(buf, FILE_WRITE)) { // filename needs to be in char
      Serial.println(F("file.open failed"));
      // TODO: mission abort;
    }
    file.rewind();

    while(file.available()){ // file is available
      if(Serial.available()){
        String serIn = Serial.readStringUntil('\n');
        if (serIn == "Pause"){
          waitUntilReceive("Resume");
        }
      }
      while(Serial.availableForWrite() < 40);
      char line[40];
      int data = file.fgets(line, sizeof(line));
      //char line = file.read();
      Serial.print(line);
    }
    //file.close(); // close the file
    while(Serial.availableForWrite() < 6000); //Wait till 6000 bytes of space is left in out buffer
    Serial.println("Raw data send complete");
    
    Serial.println("Test complete - Start saving to file");
  }
  else{
    Serial.println("Invalid weight, abolish");
    letMouseOut(ID_2);
    lastExitTime = millis();
  }
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
  Serial.println("LOGGER: Test complete");
  clear_serial_buffer(Serial1);
  clear_serial_buffer(Serial2);
}
