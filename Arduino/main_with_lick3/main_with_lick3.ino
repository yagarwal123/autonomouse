
#include <Servo.h>
#include <TimeLib.h>
#include "run_test.h"
#include "dop.h"
#include "read_id.h"
#include "check_id_exist.h"
#include "HX711.h"
#include "load_cell.h"
#include "clear_serial_buffer.h"
#define LOADCELL_DOUT_PIN  20
#define LOADCELL_SCK_PIN  19
#define calibration_factor 457 //This value is obtained using the SparkFun_HX711_Calibration sketch


// define objects for door
Servo door_one;  // create servo object to control a servo
Servo door_two; // twelve servo objects can be created on most boards

// define constants for RFID
const int noMouse = 2;
String KNOWNTAGS[noMouse] = {"0007A0F7C4", "0000000000"};
String TAGNAMES[noMouse] = {"Stuart", "Little"};
String ID, ID2;

// objects and constants for weighing
HX711 scale;
float weight;

// Variables for the lick and reward system
int rewardPin = 32;
int lickPin = A13;
int THRESHOLD = 100;

// to sync time
time_t getTeensy3Time()
{
  return Teensy3Clock.get();
}

//------------------------------------------------------------------------------
void printField(Print* pr, char sep, uint8_t v) {
  if (sep) {
    pr->write(sep);
  }  
  if (v < 10) {
    pr->write('0');
  }
  pr->print(v);
}
//------------------------------------------------------------------------------  
void printNow(Print* pr) {
  pr->print(year());
  printField(pr, '-', month());
  printField(pr, '-', day());  
  printField(pr, ' ', hour());
  printField(pr, ':', minute());
  printField(pr, ':', second());
}


// function to finalise test
// TODO: update data, savings and file transfers
void end_test(String ID, int noMouse){
  Serial.println("Test ends");  
   // clear buffer for antenna 1
  clear_serial_buffer(Serial1);

  // let mouse out
  door_open(door_two);
  door_open(door_one);
  // when antenna one detects mouse
    ID = read_id(Serial1);
  while (ID.length() != 10) {
    ID = read_id(Serial1);
    //delay(150); // a delay is needed here to read, >150??? no need of delay here
  }
  Serial.println(ID);
  String mouseName = check_id_exist(ID, KNOWNTAGS, TAGNAMES, noMouse);
  Serial.print(mouseName);
  Serial.println(" is out");
  Serial.print(F("DateTime::now "));
  printNow(&Serial);
  Serial.println();
  clear_serial_buffer(Serial1);
  Serial.println("All done");
}


void setup()
{
  // set the Time library to use Teensy 3.0's RTC to keep time
  setSyncProvider(getTeensy3Time);

  if (timeStatus()!= timeSet) {
    Serial.println("Unable to sync with the RTC");
    return;
  }
  
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  door_one.attach(2);
  door_close(door_one);
  door_two.attach(23);
  door_close(door_two);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

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

// ----------------------------- START OF ROUND ---------  
  // check antenna 1
  ID = read_id(Serial1);
  while (ID.length() != 10) {
    ID = read_id(Serial1);
    //delay(150); // a delay is needed here to read, >150??? no need of delay here
  }
  Serial.println(ID);
  String mouseName = check_id_exist(ID, KNOWNTAGS, TAGNAMES, noMouse);
  Serial.println(mouseName);
  while (mouseName == "Mouse does not exist") {
      ID = read_id(Serial1);
      while (ID.length() != 10) {
        ID = read_id(Serial1);
      }
      mouseName = check_id_exist(ID, KNOWNTAGS, TAGNAMES, noMouse);
      Serial.println(mouseName);
  } // if mouse does not exist in database - raise error
  door_open(door_one); // if mouse exists in database, open the door
  
  // clear buffer has no use here
  // checks second antenna and see if tag exists
  ID2 = read_id(Serial2);
  while(ID2.length() != 10){
    ID2 = read_id(Serial2); // case of no tag or unknown tag present
  }
  // if tag is recognised
  Serial.println(ID2);
  Serial.println(mouseName);
  while (ID2 != ID) { // in case of a different mouse
    // keep checking
    ID2 = read_id(Serial2);
    while(ID2.length() != 10){
      ID2 = read_id(Serial2); // case of no tag or unknown tag present
    }
  }
  // clear buffer for antenna 1
  clear_serial_buffer(Serial1);

  // reset scale and allow access
  scale.tare();
  door_close(door_one);
  Serial.println("opening door 2");
  door_open(door_two);

  // record mouse entrace
  Serial.print("Entering: ");
  Serial.println(ID);
  Serial.print(F("DateTime::now "));
  printNow(&Serial);
  Serial.println();

  // take the weight
  weight = load_cell(scale); // to be calibrated
  Serial.print(mouseName);
  Serial.print(" weights: ");
  Serial.print(weight);
  Serial.println("g");

  if(weight < 40){ // run test
    Serial.println("closing door 2, start test");
    door_close(door_two);
  
    int liquidAmount = 500; // command from raspi
    run_test(lickPin, THRESHOLD, rewardPin, liquidAmount);
    Serial.println("Test complete");
    //end test
    end_test(ID, noMouse);
  }
  else{
    Serial.println("Invalid weight, abolish");
    end_test(ID, noMouse);
  }
   
   // clear buffer for antenna 1
  clear_serial_buffer(Serial1);
}
