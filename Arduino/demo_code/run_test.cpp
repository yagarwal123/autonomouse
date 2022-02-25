#include "SdFat.h"
#include "run_test.h"
#include "deliver_reward.h"
#include "lick.h"
#include "HX711.h"
#include "load_cell.h"
#include "TeensyTimerTool.h"
#include "dop.h"
using namespace TeensyTimerTool; 

PeriodicTimer t1; // timer to run periodic serial print
PeriodicTimer t2; // timer to run periodic lick read and print
PeriodicTimer t3; // timer to run periodic save to file
PeriodicTimer t4; // timer to run periodically check TTL pulse

unsigned long responseTime = 0;
unsigned long downTime = 0;
int lickTime;
//unsigned long WAITTIME = 5000;
unsigned long RES = 2500;
int lickCheck = 0;

FsFile file;

void callback1(int *sensorAddr){ // to print out sensorValue in regular interval
  //Serial.print("display: ");
  Serial.println(*sensorAddr);
  }

void callback2(int lickPin, int* sensorAddr) // reads sensor value 
{
  *sensorAddr = analogRead(lickPin);
  //Serial.println(*sensorAddr);
  //Serial.println("r");
  }

void callback3(int* sensorAddr, unsigned long* timePt, FsFile* pr){ // saves sensor value at regular interval to pr
  pr->print(millis() - *timePt);
  pr->print(", ");
  pr->println(*sensorAddr);
  }


void callback4(const int TTL_PIN){ // saves sensor value at regular interval to pr
  if(digitalRead(TTL_PIN)==HIGH){
    Serial.print("TTL - ");
    Serial.println(millis());
  } // checking TTL pulse
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

void run_test(Servo door_two, String ID_2, HX711 scale, int TTL_PIN, int lickPin, int rewardPin){
  float weight;
  t4.begin([=]{callback4(TTL_PIN);}, 1ms);
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
    Serial.println("closing door 2, start test");
    door_close(door_two);

    // create file
    String fileName = ID_2 + "_"+millis()+".txt";
    Serial.println(fileName);
    char buf[30];
    fileName.toCharArray(buf, 30);
    // Remove old version to set create time.
//    if (sd.exists(fileName)) {
//      Serial.println("Duplicate file!!!");
//    }

    if (!file.open(buf, FILE_WRITE)) { // filename needs to be in char
      Serial.println(F("file.open failed"));
      // TODO: mission abort;
    }
    
    // Print current date time to file.
    file.print(F("Test file at: "));
    //printNow(&file);
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

    Serial.print("Recieved information - Liquid Amount - ");Serial.println(liquidAmount);
    Serial.print("Recieved information - Lick Threhold - ");Serial.println(THRESHOLD);
    Serial.print("Recieved information - Inter trial interval - ");Serial.println(WAITTIME);
    
    int sensorValue = 0;
    int* sensorPt = &sensorValue; // must define pointer, cannot just pass address
    unsigned long startTime = 0;
    unsigned long* timePt = &startTime; // pointer to start time of test
    int i=0;
    int noLickCounter=0;// counts the number of no licks - stops after no licks found in 5 consequtive trials
    // actual number need to be confirmed

    FsFile* pr = &file;
    // lambda function, pass in outerscope
    // define timers
    t1.begin([=]{callback1(sensorPt);}, 15ms, false); //every 100ms print to serial
    t2.begin([=]{callback2(lickPin, sensorPt);}, 1ms, false); // reads lickPin every 50ms
    t3.begin([=]{callback3(sensorPt, timePt, pr);}, 1ms); // saves amplitude every 1ms
    
    
    Serial.print("Starting test now - "); Serial.println(millis());
    pr->println(millis()); // write start time in file DELETE ONE
    //for(int i=1; i<11; i++){
    while(noLickCounter<5){
      i++; // increment trial number
      //Serial.print("Trial ");
      //Serial.println(i);
      lickTime = -1; // time takes to lick: if not licked return -1
      lickCheck = 0; // time taken to lick from stimulus onset
      startTime = millis(); // record start time
      responseTime = startTime + RES; // acceptable responese time to stimulus
      pr->println(millis()); // write start time in file DELETE ONE
      t1.start(); // start 
      //t3.start(); // start saving to file
      //Serial.println(startTime);
      while(millis() < responseTime){// response period
        if (lickTime == -1){ // if mouse hasn't responded
          lickCheck = read_lick(lickPin, THRESHOLD, &sensorValue); // read_lick returns time licked
          if (lickCheck > 0){
            t2.start(); // start reading at longer intervals if mouse has licked
            lickTime = lickCheck - startTime;
            deliver_reward(rewardPin, liquidAmount);// if mouse has licked during response period
            noLickCounter=0; // reset noLickCounter
            }
          }
        }
        downTime = millis() + WAITTIME; // count 5s from now
  
      t1.stop();// stop timers whether or not there was licking
      if (lickTime < 0){ // start reading at longer intervals if mouse hasnt licked
        t2.start();
        noLickCounter++;
      }
      Serial.print("Lick Sensor - Trial ");
      Serial.print(i);
      Serial.print(" - Time ");
      Serial.println(lickTime);
      t1.start(); // start timer again
      
      while(millis() < downTime){ // downtime of sensor
        // other processes - communications etc
      }
      // stop timers
      t1.stop();
      t2.stop();
      //t3.stop();
    }
    t3.stop();
    file.close(); // close the file

    Serial.println("Sending raw data");
    //t4.stop(); // stop reading TTL pulse
    // TODO: send file to PC through Serial
    //file.rewind();
    while (true){
      while(!Serial.available());
      String serIn = Serial.readStringUntil('\n');
      if (serIn == "Camera closed"){
        break;
      }
    }


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
  }

    
  t4.stop();
}
