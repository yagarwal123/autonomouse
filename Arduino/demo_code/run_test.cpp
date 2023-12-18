  /*****************************************************************************
  Second main piece of function for experiment result collection.
  Has timers and automatically triggers data saving to the teensy SD card.
  Delivers stimulation, calls lick detection and delivers reward.
  Ran once for each time a mouse is in the testing chamber.
  Loops through trials.
  *****************************************************************************/

#include "SdFat.h"
#include "run_test.h"
#include "deliver_reward.h"
#include "lick.h"
#include "TeensyTimerTool.h"
#include "HX711.h"
#include "stimulus.h"
using namespace TeensyTimerTool; 

PeriodicTimer t1; // timer to run periodic serial print
PeriodicTimer t2; // timer to run periodic lick read and print
PeriodicTimer t3; // timer to run periodic save to file

unsigned long responseTime = 0;
unsigned long downTime = 0;
int lickTime;
//unsigned long WAITTIME = 5000;
//unsigned long RES = 2500;
int lickCheck = 0;

bool buttonStateRising;
bool lastButtonStateRising=0;

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

void callback3(int TTL_PIN, int* sensorAddr, unsigned long* timePt, FsFile* pr){ // saves sensor value at regular interval to pr
  pr->print(millis() - *timePt);
  pr->print(", ");
  pr->print(*sensorAddr);
  pr->print(", ");
  buttonStateRising = digitalRead(TTL_PIN);
  if ((buttonStateRising == HIGH) && (lastButtonStateRising == LOW)) {
    pr->println(millis());
  }
  else{
    pr->println(0);
  }
  lastButtonStateRising = buttonStateRising;
  }
/*
int* convertStrtoArr(char* str){
    // get length of string str
    int str_length = sizeof(str)/ sizeof(str[0]);
 
    // create an array with size as string
    // length and initialize with 0
    int arr[str_length] = { 0 };
 
    int j = 0, i;
    int size = sizeof(str)/ sizeof(str[0]);
    // Traverse the string
    for (i = 0; i<size; i++) {
 
        // if str[i] is ', ' then split
        if (str[i] == ',')
            continue;
         if (str[i] == ' '){
            // Increment j to point to next
            // array location
            j++;
        }
        else {
 
            // subtract str[i] by 48 to convert it to int
            // Generate number by multiplying 10 and adding
            // (int)(str[i])
            arr[j] = arr[j] * 10 + (str[i] - 48);
        }
    }
    return arr;
 
    cout<<"arr[] ";
    for (i = 0; i <= j; i++) {
        cout << arr[i] << " ";
        sum += arr[i]; // sum of array
    }
    cout<<endl;
    // print sum of array
    cout<<sum<<endl;
    
}
*/

void run_test(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int *stimPin, int liquidAmount, int RES, int stimProb, unsigned long stimDuration, int *oStim, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin){
  int sensorValue = 0;
  int* sensorPt = &sensorValue; // must define pointer, cannot just pass address
  unsigned long startTime = 0;
  unsigned long* timePt = &startTime; // pointer to start time of test
  int i=0; // trial counter
  bool testOngoing = 1; // stops test on command
  bool punish = false; // whether to push mouse by having larger ITI
  bool target = false; // if odour pattern contains target(s)
  //int noLickCounter = 0; // counts the number of no licks - stops after no licks found in 5 consequtive trials
  // actual number need to be confirmed

  int *stimulus;
  
  // lambda function, pass in outerscope
  // define timers
  t1.begin([=]{callback1(sensorPt);}, 100ms, false); //every 100ms print to serial
  t2.begin([=]{callback2(lickPin, sensorPt);}, 1ms, false); // reads lickPin every 50ms
  Serial.print("Starting test now - "); Serial.println(millis());
  while (digitalRead(TTL_PIN)==LOW);
  t3.begin([=]{callback3(TTL_PIN, sensorPt, timePt, pr);}, 1ms); // saves amplitude every 1ms
  
  pr->println(millis()); // write start time in file DELETE ONE
  //for(int i=1; i<11; i++){
  //t1.start();
  while(testOngoing){
    i++; // increment trial number
    //Serial.print("Trial ");
    //Serial.println(i);
    lickTime = -1; // time takes to lick: if not licked return -1
    lickCheck = 0; // time taken to lick from stimulus onset
    
    stimulus = start_stimulus(stimPin, oStim, nStim, stimProb, stimDuration); //address of stimulus
    
    startTime = millis(); // record start time
    responseTime = startTime + RES; // acceptable responese time to stimulus
    //pr->println(millis()); // write start time in file DELETE ONE
    t1.start(); // start 
    //t3.start(); // start saving to file
    //Serial.println(startTime);
    punish = false;
    while(millis() < responseTime){// response period
      if (lickTime == -1){ // if mouse hasn't responded
        lickCheck = read_lick(lickPin, THRESHOLD, &sensorValue); // read_lick returns time licked
        if (lickCheck > 0){
          t2.start(); // start reading at longer intervals if mouse has licked
          lickTime = lickCheck - startTime;
          if (stimulus[0]==1 || target == true){ // if matches target stimulus
            deliver_reward(rewardPin, liquidAmount);// if mouse has licked during response period
          }else{
            punish = true;
          }
          //noLickCounter=0; // reset noLickCounter
          }
        }
      if (millis() - startTime > stimDuration){ // stimDuration has to be shorter than response time
        // stop stimulus (olfaction only)
        stop_stimulus(stimPin, nStim); 
        }
      }
      
      if (punish==true){
        downTime = millis() + WAITTIME + punishtime;// wait for longer if false positive response
      }else{
        downTime = millis() + WAITTIME;
        } // start of DOWNTIME

    t1.stop();// stop timers whether or not there was licking
    if (lickTime < 0){ // start reading at longer intervals if mouse hasnt licked
      t2.start();
      //noLickCounter++;
    }
    Serial.print("Lick - Stimulus "); Serial.print(*stimulus); Serial.print(" - Trial ");
    Serial.print(i);
    Serial.print(" - Time ");
    Serial.println(lickTime);
    
    t1.start(); // start timer again
    //digitalWrite(pumpPin, HIGH); // start pumping out air

    while(millis() < downTime){ // downtime of sensor
      if(Serial.available()){
        String serIn = Serial.readStringUntil('\n');
        if (serIn == "Reward"){
          deliver_reward(rewardPin, liquidAmount); // also customise liquid drop here
        }
        if(serIn == "End"){
          testOngoing = 0;
        }
        if(serIn == "liquid"){
          while (!Serial.available());
          liquidAmount = Serial.readStringUntil('\n').toInt();
        }
        if(serIn == "th"){
          while (!Serial.available());
          THRESHOLD = Serial.readStringUntil('\n').toInt();
        }
        if(serIn == "wait"){
          while (!Serial.available());
          WAITTIME = Serial.readStringUntil('\n').toInt();
        }
        if(serIn == "punish"){
          while (!Serial.available());
          punishtime = Serial.readStringUntil('\n').toInt();
        }
        if(serIn == "resp"){
          while (!Serial.available());
          RES = Serial.readStringUntil('\n').toInt();
        }
        if(serIn == "stim"){
          while (!Serial.available());
          stimProb = Serial.readStringUntil('\n').toInt();
        }
        if(serIn == "oStim"){
          while (!Serial.available());
          //oStim = convertStrtoArr(Serial.readStringUntil('\n'));
          *oStim = Serial.readStringUntil('\n').toInt(); // not sure if this is giving one int or an array TODO:fix
        }
        if(serIn == "target"){
          while (!Serial.available());
          target = Serial.readStringUntil('\n').toInt();
        }
        if(serIn == "dur"){
          while (!Serial.available());
          stimDuration = Serial.readStringUntil('\n').toInt();
        }
      }
    }
    // stop timers
    t1.stop();
    t2.stop();
    //t3.stop();
    digitalWrite(pumpPin, LOW); // stop pumping out air
  }
  //t1.stop();
  t3.stop();
  Serial.println("Stop recording");
}

