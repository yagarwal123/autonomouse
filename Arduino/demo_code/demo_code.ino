 #include <Servo.h>
#include <TimeLib.h>
#include "run_test.h"
#include "dop.h"
#include "HX711.h"
#include "load_cell.h"
#include "clear_serial_buffer.h"
#include "SdFat.h"
#include "time_functions.h"
#include "deliver_reward.h"
//#include "TeensyTimerTool.h"
#define LOADCELL_DOUT_PIN  20
#define LOADCELL_SCK_PIN  19
#define calibration_factor 1019 //This value is obtained using the SparkFun_HX711_Calibration sketch
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
String ID;

// objects and constants for weighing
HX711 scale;
float weight;

// Variables for the lick and reward system
int rewardPin = 32;
int lickPin = A1;
int TTL_PIN = 33;

unsigned long INTERVAL_BETWEEN_TESTS = 60*1e3;       //One minute before the same mouse is let in
unsigned long lastExitTime = 0;
String lastMouse = "";
int d_count;

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
  door_open(door_one);
  door_close(door_two);
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

  //Needs to be an unconnected pin
  randomSeed(analogRead(0));
  
  //Setting up the pins for the reward system
  pinMode(rewardPin, OUTPUT);
  digitalWrite(rewardPin, LOW);
    // pin for TTL pulse camera
  pinMode(TTL_PIN, INPUT);
  //attachInterrupt(digitalPinToInterrupt(TTL_PIN), callback4, RISING);

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
  // refill syringe function
  if(Serial.available()){
    String serIn = Serial.readStringUntil('\n');
    if (serIn == "Refill"){
      digitalWrite(rewardPin, HIGH);
      waitUntilReceive("Stop");
      digitalWrite(rewardPin, LOW);
    }
  }

  
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
  scale.tare(); // reset scale again
  door_close(door_one);
  
  // or take weight here
  for (int i = 0; i < 10; i++){
    String serOut = "";
    float weight = scale.get_units();
    weight= round(weight*10)/10;
    serOut = serOut + "Weight Sensor - Weight " + weight + "g";
    Serial.println(serOut);
    delay(500); //So the readings are spaced out. TODO: To discuss
  }

  door_open(door_two);
  lastMouse = ID_2;

  // lure mouse
  deliver_reward(rewardPin, 100);

  // run test
  
  // String serOut = "";
  // serOut = serOut + "Weight Sensor - Weight " + weight + "g - Time " + millis();
  // Serial.println(serOut);
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
  file.print(F("amplitude, "));
  file.println(F("TTL"));
  
  Serial.print("Send parameters: Incoming mouse ID - "); Serial.println(ID_2);
  while (!Serial.available());
  int THRESHOLD = Serial.readStringUntil('\n').toInt();
  while (!Serial.available());
  int liquidAmount = Serial.readStringUntil('\n').toInt();
  while (!Serial.available());
  int WAITTIME = Serial.readStringUntil('\n').toInt();
  while (!Serial.available());
  int responseTime = Serial.readStringUntil('\n').toInt();
  while (!Serial.available());
  int stimProb = Serial.readStringUntil('\n').toInt();
  Serial.print("LOGGER: Received - Liquid Amount - ");Serial.println(liquidAmount);
  Serial.print("LOGGER: Received - Lick Threhold - ");Serial.println(THRESHOLD);
  Serial.print("LOGGER: Received - Inter trial interval - ");Serial.println(WAITTIME);
  Serial.print("LOGGER: Received - Response Time - ");Serial.println(responseTime);
  Serial.print("LOGGER: Received - Stimulus Probability - ");Serial.println(stimProb);
  
  run_test(TTL_PIN, lickPin, THRESHOLD, rewardPin, liquidAmount, responseTime, stimProb, &file, WAITTIME, &scale); // write to file during test
  file.close(); // close the file
  
  waitUntilReceive("Camera closed");

  letMouseOut(ID_2);
  lastExitTime = millis();

  Serial.println("Test complete - Start saving to file");

  Serial.println("Sending raw data");
  waitUntilReceive("Ready"); // wait for python to be ready to receive data

  // open file again
  if (!file.open(buf, FILE_WRITE)) { // filename needs to be in char
    Serial.println(F("file.open failed"));
    // TODO: error handling
  }
  file.rewind();
  d_count = 0;
  while(file.available()){ // file is available
    if(Serial.available()){ // python reads slower than teensy sends wait for python to clear in buffer
      String serIn = Serial.readStringUntil('\n');
      if (serIn == "Pause"){
        waitUntilReceive("Resume");
      }
    }
    while(Serial.availableForWrite() < 40);
    char line[40];
    file.fgets(line, sizeof(line));
    //char line = file.read();
    Serial.print(line);
    d_count++;
    if (d_count > 5){
      delay(1);
      d_count = 0;
    }
    //delay(1);
  }
  //file.close(); // close the file
  while(Serial.availableForWrite() < 6000); //Wait till 6000 bytes of space is left in out buffer
  Serial.println("Raw data send complete");
  waitUntilReceive("Reconnected");
    
  //while (door1Check() != ID_2){}
  //door_close(door_one);
  Serial.println("Waiting for the save to complete");
  waitUntilReceive("Save complete");

  Serial.println("LOGGER: Test complete");
  clear_serial_buffer(Serial1);
  clear_serial_buffer(Serial2);
}
