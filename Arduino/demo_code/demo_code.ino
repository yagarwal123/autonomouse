/*****************************************************************************
  Main C code, calls al the functions and runs the loop of commands whcih overarchs all the automated operations in the setup
*****************************************************************************/

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
#include "wait_for_serial.h"
//#include "TeensyTimerTool.h"
#define LOADCELL_DOUT_PIN  20
#define LOADCELL_SCK_PIN  19
#define calibration_factor -1057.57 //This value is obtained using the SparkFun_HX711_Calibration sketch
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
// TEMPORARY DEFINITION OF SCENARIO > LATER WILL ADD TO GUI OF PYTHON CODE SO USER CAN EASILY CHANGE
// 0 = Habituation
// 1 = Pre-learning 1
// 2 = Pre-learning 2
// 3 = Pre-learning 3
// 4 = Learning
int SCENARIO = 1;

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
int lickPin = A14;
int TTL_PIN = 33;
int stimPin[] = {8, 9, 13}; // to be extended to more pins after writing python code, first element is sound
int pumpPin = 12;
int LED_PIN = 13; // JP for testing

//unsigned long INTERVAL_BETWEEN_TESTS = 60 * 1e3;     //One minute before the same mouse is let in
unsigned long INTERVAL_BETWEEN_TESTS = 10;     // JP 

unsigned long lastExitTime = 0;
String lastMouse = "";
int d_count;

String door1Check() {
  if (Serial1.available()) {
    ID = Serial1.readStringUntil('\r');
    unsigned long recordTime = millis();
    String serOut = "";
    serOut = serOut + "Door Sensor - ID " + ID + " - Door 1 - Time " + recordTime;
    Serial.println(serOut);
  }
  else {
    ID = "";
  };
  return ID;
}

String door2Check() {
  if (Serial2.available()) {
    ID = Serial2.readStringUntil('\r');
    unsigned long recordTime = millis();
    String serOut = "";
    serOut = serOut + "Door Sensor - ID " + ID + " - Door 2 - Time " + recordTime;
    Serial.println(serOut);
  }
  else {
    ID = "";
  };
  return ID;
}

void waitUntilReceive(String msg) { // waits for message from python
  while (true) {
    waitForSerial(door_one, door_two);
    String serIn = Serial.readStringUntil('\n');
    if (serIn == msg) {
      break;
    }
  }
}

void letMouseOut(String ID_2) {
  clear_serial_buffer(Serial2);
  //door_open(door_two);
  door_open(door_two, 2); // 20230719
  while (door2Check() != ID_2) {} // either this or just open whenever something is in serial 2
  //door_open(door_one);
  door_open(door_one, 1); // 20230719
  door_close(door_two, 1); // True for slower door
}

void setup()
{
  Serial.begin(9600); // serial port to communicate with teensy 4.1
  Serial1.begin(9600); // serial port to read from sensor closest to home cage
  Serial2.begin(9600); // serial port to read from sensor closest to trainbox
  door_one.attach(2);
  door_two.attach(23);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

  //Needs to be an unconnected pin
  randomSeed(analogRead(17));

  // pin for testing
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  //Setting up the pins for the reward system
  pinMode(rewardPin, OUTPUT);
  digitalWrite(rewardPin, LOW);
  // pin for TTL pulse camera
  pinMode(TTL_PIN, INPUT);
  //attachInterrupt(digitalPinToInterrupt(TTL_PIN), callback4, RISING);

  // setup olfaction pins
  for (int i = 0; i < (int)(sizeof(*stimPin) / sizeof(stimPin[0])); i++) {
    pinMode(stimPin[i], OUTPUT);
    Serial.print("setting up pins: ");
    Serial.println(stimPin[i]);
  }

  // pump pin
  pinMode(pumpPin, OUTPUT);
  digitalWrite(pumpPin, LOW);

  // time
  setSyncProvider(getTeensy3Time);

  if (timeStatus() != timeSet) {
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

  while (! Serial);       //Wait for python read to begin
  Serial.println("LOGGER: Starting Experiment");


  //---------------------------------------
  //door_open(door_one);
  //Serial.print("open door 1: pre: ");
  //Serial.print(door_one.read());
  door_open(door_one, 1); // 20230719
  //Serial.print(" post: ");
  //Serial.println(door_one.read());
  door_close(door_two, 0);
  // door 1 open and door 2 close
  //---------------------------------------

}

void loop()
{
  //check_gui(door_one, door_two);
  // refill syringe function
  if (Serial.available()) {
    String serIn = Serial.readStringUntil('\n');
    if (serIn == "Refill") {
      digitalWrite(rewardPin, HIGH);
      //waitUntilReceive("Stop");
      while (true) {
        String serIn = Serial.readStringUntil('\n');
        if (serIn == "Stop") {
          break;
        }
      }
      digitalWrite(rewardPin, LOW);
    }
    if (serIn == "door1open") {
      emergency_door_open_close(door_one, 1, 1);
    }
    if (serIn == "door1close") {
      emergency_door_open_close(door_one, 1, 2);
    }
    if (serIn == "door2open") {
      emergency_door_open_close(door_two, 2, 1);
    }
    if (serIn == "door2close") {
      emergency_door_open_close(door_two, 2, 2);
    }
    if (serIn == "Scenario0") {
      SCENARIO = 0;
    }
    if (serIn == "Scenario1") {
      SCENARIO = 1;
    }
    if (serIn == "Scenario2") {
      SCENARIO = 2;
    }
    if (serIn == "Scenario3") {
      SCENARIO = 3;
    }
  }


  // constantly checks until a known mouse appears
  // can make this an interrupt or something

  String ID_1 = door1Check(); // subfunction of demo_code
  String ID_2 = door2Check(); // subfunction of demo_code

  if (( SCENARIO == 0 ) || ( SCENARIO == 2 )) {

    door_open(door_one, 1);
    door_open(door_two, 2);
    Serial.println("LOGGER: Scenario 0");

    ID_2 = "999";
    Serial.print("Check whether to start test - "); Serial.println(ID_2);
    while (true) {
      waitForSerial(door_one, door_two);
      String serIn = Serial.readStringUntil('\n');
      if (serIn == "Do not start") {
        clear_serial_buffer(Serial1);
        clear_serial_buffer(Serial2);
        return;
      }
      else if (serIn == "Start experiment") {
        break;
      }
    }

    //int THRESHOLD = 0;
    int THRESHOLD = 100;
    int liquidAmount = 200;
    int WAITTIME = 0;
    int punishtime = 0;
    //int responseTime = 0;
    int responseTime = 3000;
    int stimProb[] = {0, 1, 1}; // use default olfactory stim for now, need to be the same size as stimPin
    unsigned long stimDuration = 2000; // use default for now - get from python later
    int nStim = sizeof(stimProb); // number of pins used for stimulus

    //run_test(TTL_PIN, lickPin, THRESHOLD, rewardPin, stimPin, liquidAmount, responseTime, stimProb, stimDuration, nStim, &file, WAITTIME, punishtime, &scale, pumpPin); // write to file during test
    SCENARIO = run_test_habituate(TTL_PIN, lickPin, THRESHOLD, rewardPin, stimPin, liquidAmount, responseTime, stimProb, stimDuration, nStim, &file, WAITTIME, punishtime, &scale, pumpPin, SCENARIO, LED_PIN, door_one, door_two); // write to file during test
    Serial.print("Finished run_test_habituate. SCENARIO="); Serial.println(SCENARIO);

    //if (SCENARIO == 1){
    // 
    //}
  }

  else if (SCENARIO == 1) {
    //TODO: dealing with rollover
    if ( (ID_2 == lastMouse) && ( (millis() - lastExitTime) < INTERVAL_BETWEEN_TESTS ) ) {
      Serial.println("Do not let same mouse in again");
      return;
    }

    if ( (ID_2.length() == 0) || (ID_1.length() != 0) ) {      
      return;
    }

    Serial.print("ID1:");Serial.print(ID_1);Serial.print(" ID2:");Serial.println(ID_2);

    Serial.print("Check whether to start test - "); Serial.println(ID_2);
    while (true) {
      waitForSerial(door_one, door_two);
      String serIn = Serial.readStringUntil('\n');
      if (serIn == "Do not start") {
        clear_serial_buffer(Serial1);
        clear_serial_buffer(Serial2);
        return;
      }
      else if (serIn == "Start experiment") {
        break;
      }
    }
    door_close(door_one, 0);

    // or take weight here
    weight = scale.get_units();
    while (weight < 10) {  //wait for mouse to get on
      //check_gui(door_one, door_two);
      if (Serial.available()) {
        String serIn = Serial.readStringUntil('\n');
        if (serIn == "Manual Start") {
          break;
        }
      }
      Serial.print("LOGGER: Mouse not on - "); Serial.println(weight);
      weight = scale.get_units();
    }
    for (int i = 0; i < 10; i++) {
      weight = scale.get_units();
      Serial.print("Weight Sensor - Weight "); Serial.print(weight, 1); Serial.println("g");
      delay(500); //So the readings are spaced out. TODO: To discuss
    }

    door_open(door_two, 2); //20230719
    lastMouse = ID_2;

    // lure mouse
    deliver_reward(rewardPin, 100);

    // run test

    // String serOut = "";
    // serOut = serOut + "Weight Sensor - Weight " + weight + "g - Time " + millis();
    // Serial.println(serOut);
    unsigned w_zero = 0;
    while (true) {
      if (scale.get_units() < 2) {
        w_zero++;
        if (w_zero >= 15) {
          break;
        };
      }
      else {
        w_zero = 0;
      };
      if (Serial.available()) {
        String serIn = Serial.readStringUntil('\n');
        if (serIn == "Manual Start") {
          break;
        }
      }
    }
    Serial.println("LOGGER: Closing door 2, start test");
    door_close(door_two, 0);
    //t4.start();

    // create file
    String fileName = ID_2 + month() + "_" + day() + "_" + hour() + "_" + minute() + "_" + second() + ".txt";
    Serial.print("LOGGER: Filename - "); Serial.println(fileName);
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

    //check_gui(door_one, door_two);
    Serial.print("Send parameters: Incoming mouse ID - "); Serial.println(ID_2);
    waitForSerial(door_one, door_two);
    int THRESHOLD = Serial.readStringUntil('\n').toInt();
    waitForSerial(door_one, door_two);
    int liquidAmount = Serial.readStringUntil('\n').toInt();
    waitForSerial(door_one, door_two);
    int WAITTIME = Serial.readStringUntil('\n').toInt();
    waitForSerial(door_one, door_two);
    int punishtime = Serial.readStringUntil('\n').toInt();
    waitForSerial(door_one, door_two);
    int responseTime = Serial.readStringUntil('\n').toInt();
    waitForSerial(door_one, door_two);
    int stimProb[] = {0, 1, 1}; // use default olfactory stim for now, need to be the same size as stimPin
    stimProb[0] = Serial.readStringUntil('\n').toInt();
    unsigned long stimDuration = 2000; // use default for now - get from python later
    int nStim = sizeof(stimProb); // number of pins used for stimulus
    if (nStim != sizeof(stimPin)) {
      Serial.println("STIM ARRAY NOT SAME SIZE AS STIMPIN - please check and restart");
      while (true); //Do nothing forever
    }

    Serial.print("LOGGER: Received - Liquid Amount - "); Serial.println(liquidAmount);
    Serial.print("LOGGER: Received - Lick Threhold - "); Serial.println(THRESHOLD);
    Serial.print("LOGGER: Received - Inter trial interval - "); Serial.println(WAITTIME);
    Serial.print("LOGGER: Received - Punishment Time - "); Serial.println(punishtime);
    Serial.print("LOGGER: Received - Response Time - "); Serial.println(responseTime);
    Serial.print("LOGGER: Received - Stimulus Probability - "); Serial.println(stimProb[0]); // change line to print whole array
    // maybe also a line for stim duration

    SCENARIO = run_test(TTL_PIN, lickPin, THRESHOLD, rewardPin, stimPin, liquidAmount, responseTime, stimProb, stimDuration, nStim, &file, WAITTIME, punishtime, &scale, pumpPin, SCENARIO, door_one, door_two); // write to file during test
    Serial.print("Finished run_test. SCENARIO="); Serial.println(SCENARIO);
    
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
    while (file.available()) { // file is available
      if (Serial.available()) { // python reads slower than teensy sends wait for python to clear in buffer
        String serIn = Serial.readStringUntil('\n');
        if (serIn == "Pause") {
          waitUntilReceive("Resume");
        }
      }
      while (Serial.availableForWrite() < 40);
      char line[40];
      file.fgets(line, sizeof(line));
      //char line = file.read();
      Serial.print(line);
      d_count++;
      if (d_count > 5) {
        delay(1);
        d_count = 0;
      }
      //delay(1);
    }
    //file.close(); // close the file
    while (Serial.availableForWrite() < 6000); //Wait till 6000 bytes of space is left in out buffer
    Serial.println("Raw data send complete");
    waitUntilReceive("Reconnected");

    //while (door1Check() != ID_2){}
    //door_close(door_one);
    Serial.println("Waiting for the save to complete");
    waitUntilReceive("Save complete");

    Serial.println("LOGGER: Test complete");
    clear_serial_buffer(Serial1);
    clear_serial_buffer(Serial2);
  } // else if (!(SCENARIO == 0)) {
}
