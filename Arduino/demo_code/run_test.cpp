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
bool lastButtonStateRising = 0;

void callback1(int *sensorAddr) { // to print out sensorValue in regular interval
  //Serial.print("display: ");
  Serial.println(*sensorAddr);
}

void callback2(int lickPin, int* sensorAddr) // reads sensor value
{
  *sensorAddr = analogRead(lickPin);
  //Serial.println(*sensorAddr);
  //Serial.println("r");
}

void callback3(int TTL_PIN, int* sensorAddr, unsigned long* timePt, FsFile* pr) { // saves sensor value at regular interval to pr
  pr->print(millis() - *timePt);
  pr->print(", ");
  pr->print(*sensorAddr);
  pr->print(", ");
  buttonStateRising = digitalRead(TTL_PIN);
  if ((buttonStateRising == HIGH) && (lastButtonStateRising == LOW)) {
    pr->println(millis());
  }
  else {
    pr->println(0);
  }
  lastButtonStateRising = buttonStateRising;
}

void run_test(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin) {
  int sensorValue = 0;
  int* sensorPt = &sensorValue; // must define pointer, cannot just pass address
  unsigned long startTime = 0;
  unsigned long* timePt = &startTime; // pointer to start time of test
  int i = 0;
  bool testOngoing = 1; // stops test on command
  bool punish = false; // whether to push mouse by having larger ITI
  //int noLickCounter = 0; // counts the number of no licks - stops after no licks found in 5 consequtive trials
  // actual number need to be confirmed

  unsigned stimulus;

  // lambda function, pass in outerscope
  // define timers
  t1.begin([ = ] {callback1(sensorPt);}, 100ms, false); //every 100ms print to serial
  t2.begin([ = ] {callback2(lickPin, sensorPt);}, 1ms, false); // reads lickPin every 50ms
  Serial.print("Starting test now - "); Serial.println(millis());
  while (digitalRead(TTL_PIN) == LOW);
  t3.begin([ = ] {callback3(TTL_PIN, sensorPt, timePt, pr);}, 1ms); // saves amplitude every 1ms

  pr->println(millis()); // write start time in file DELETE ONE
  //for(int i=1; i<11; i++){
  //t1.start();
  while (testOngoing) {
    i++; // increment trial number
    //Serial.print("Trial ");
    //Serial.println(i);
    lickTime = -1; // time takes to lick: if not licked return -1
    lickCheck = 0; // time taken to lick from stimulus onset

    stimulus = start_stimulus(stimPin, nStim, stimProb, stimDuration);

    startTime = millis(); // record start time
    responseTime = startTime + RES; // acceptable responese time to stimulus
    //pr->println(millis()); // write start time in file DELETE ONE
    t1.start(); // start
    //t3.start(); // start saving to file
    //Serial.println(startTime);
    punish = false;
    while (millis() < responseTime) { // response period
      if (lickTime == -1) { // if mouse hasn't responded
        lickCheck = read_lick(lickPin, THRESHOLD, &sensorValue); // read_lick returns time licked
        if (lickCheck > 0) {
          t2.start(); // start reading at longer intervals if mouse has licked
          lickTime = lickCheck - startTime;
          if (stimulus == 1) { // TODO: match olfactory stim to response
            deliver_reward(rewardPin, liquidAmount);// if mouse has licked during response period
          } else {
            punish = true;
          }
          //noLickCounter=0; // reset noLickCounter
        }
      }
      if (millis() - startTime > stimDuration) { // stimDuration has to be shorter than response time
        // stop stimulus (olfaction only)
        //stop_stimulus(stimPin, nStim); //**** PROBLEM WITH DOORS HERE
      }
    }

    if (punish == true) {
      downTime = millis() + WAITTIME + punishtime;// wait for longer if false positive response
    } else {
      downTime = millis() + WAITTIME;
    } // start of DOWNTIME

    t1.stop();// stop timers whether or not there was licking
    if (lickTime < 0) { // start reading at longer intervals if mouse hasnt licked
      t2.start();
      //noLickCounter++;
    }
    Serial.print("Lick - Stimulus "); Serial.print(stimulus); Serial.print(" - Trial ");
    Serial.print(i);
    Serial.print(" - Time ");
    Serial.println(lickTime);

    t1.start(); // start timer again
    //digitalWrite(pumpPin, HIGH); // start pumping out air

    while (millis() < downTime) { // downtime of sensor
      if (Serial.available()) {
        String serIn = Serial.readStringUntil('\n');
        if (serIn == "Reward") {
          deliver_reward(rewardPin, liquidAmount); // also customise liquid drop here
        }
        if (serIn == "End") {
          testOngoing = 0;
        }
        if (serIn == "liquid") {
          while (!Serial.available());
          liquidAmount = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "th") {
          while (!Serial.available());
          THRESHOLD = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "wait") {
          while (!Serial.available());
          WAITTIME = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "punish") {
          while (!Serial.available());
          punishtime = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "resp") {
          while (!Serial.available());
          RES = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "stim") {
          while (!Serial.available());
          stimProb[0] = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "dur") {
          while (!Serial.available());
          stimDuration = Serial.readStringUntil('\n').toInt();
        }
      }
    }
    // stop timers
    t1.stop();
    t2.stop();
    //t3.stop();
    //digitalWrite(pumpPin, LOW); // stop pumping out air
  }
  //t1.stop();
  t3.stop();
  Serial.println("Stop recording");
}



//void run_test_habituate(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin, int SCENARIO, int LED_PIN) {
int run_test_habituate(int TTL_PIN, int lickPin, int THRESHOLD, int rewardPin, int stimPin[], int liquidAmount, int RES, int stimProb[], unsigned long stimDuration, int nStim, FsFile* pr, int WAITTIME, int punishtime, HX711 *scale, int pumpPin, int SCENARIO, int LED_PIN) {

  unsigned long startTime = 0;
  int i = 0; // trial counter
  bool testOngoing = 1; // stops test on command
  unsigned stimulus;
  int sensorValue = 0;

  lickTime = 0;

  int rewardCollected = 1; // set to 1 so that reward delivered in beginning
  if (SCENARIO == 2) { // only give reward if mouse licks (only once per trial)
    rewardCollected = 0;
  }

  while (testOngoing) {
    i++; // increment trial number
    startTime = millis(); // record start time
    responseTime = startTime + RES; // acceptable responese time to stimulus

    //Serial.print("THRESHOLD="); Serial.println(THRESHOLD);

    if (SCENARIO == 2) { // only give reward if mouse licks (only once per trial)
      rewardCollected = 0;
    }
    if (SCENARIO == 0) {
      if ( rewardCollected == 1 ) {
        deliver_reward(rewardPin, liquidAmount);// if mouse has licked during response period
        rewardCollected = 0;
      }
    }


    while (millis() < responseTime) { // response period
      sensorValue = analogRead(lickPin); // constantly read lick trace
      if (sensorValue > THRESHOLD) {
        digitalWrite(LED_PIN, HIGH);
        if (( SCENARIO == 2 ) && (rewardCollected == 0)) {
          rewardCollected = 1;
          deliver_reward(rewardPin, liquidAmount);// give reward after each lick
        }
        if (SCENARIO == 0) {
          rewardCollected = 1;
        }
      }
      else {
        digitalWrite(LED_PIN, LOW);
      }

      if (Serial.available()) {
        String serIn = Serial.readStringUntil('\n');
        Serial.print(serIn);
        if (serIn == "Reward") {
          deliver_reward(rewardPin, liquidAmount); // also customise liquid drop here
        }
        if (serIn == "End") {
          testOngoing = 0;
        }
        if (serIn == "liquid") {
          while (!Serial.available());
          liquidAmount = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "th") {
          while (!Serial.available());
          THRESHOLD = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "wait") {
          while (!Serial.available());
          WAITTIME = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "punish") {
          while (!Serial.available());
          punishtime = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "resp") {
          while (!Serial.available());
          RES = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "stim") {
          while (!Serial.available());
          stimProb[0] = Serial.readStringUntil('\n').toInt();
        }
        if (serIn == "dur") {
          while (!Serial.available());
          stimDuration = Serial.readStringUntil('\n').toInt();
        }
      }
    }

    //Serial.print("sensorValue="); Serial.println(sensorValue);

    Serial.print("Lick - Stimulus "); Serial.print(stimulus); Serial.print(" - Trial ");
    Serial.print(i);
    Serial.print(" - Time ");
    Serial.println(lickTime);



  }

  return SCENARIO;

  /*
    Serial.println("run_test_habituate");
    int sensorValue = 0;
    int* sensorPt = &sensorValue; // must define pointer, cannot just pass address
    unsigned long startTime = 0;
    unsigned long* timePt = &startTime; // pointer to start time of test
    int i=0;
    bool testOngoing = 1; // stops test on command
    bool punish = false; // whether to push mouse by having larger ITI
    //int noLickCounter = 0; // counts the number of no licks - stops after no licks found in 5 consequtive trials
    // actual number need to be confirmed

    unsigned stimulus;

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

    //stimulus = start_stimulus(stimPin, nStim, stimProb, stimDuration);

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
          if (stimulus==1){ // TODO: match olfactory stim to response
            deliver_reward(rewardPin, liquidAmount);// if mouse has licked during response period
          }else{
            punish = true;
          }
          //noLickCounter=0; // reset noLickCounter
          }
        }
      if (millis() - startTime > stimDuration){ // stimDuration has to be shorter than response time
        // stop stimulus (olfaction only)
        //stop_stimulus(stimPin, nStim); //**** PROBLEM WITH DOORS HERE
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
    Serial.print("Lick - Stimulus "); Serial.print(stimulus); Serial.print(" - Trial ");
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
          stimProb[0] = Serial.readStringUntil('\n').toInt();
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
    //digitalWrite(pumpPin, LOW); // stop pumping out air
    }
    //t1.stop();
    t3.stop();
    Serial.println("Stop recording");

  */
}
