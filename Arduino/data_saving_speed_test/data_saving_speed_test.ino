#include "TeensyTimerTool.h"
using namespace TeensyTimerTool; 
#include "SdFat.h"
#define SD_FAT_TYPE 3
#define SD_CONFIG SdioConfig(FIFO_SDIO)
SdFs sd;
FsFile file; 

PeriodicTimer t1; // timer to run periodic serial print
int val = 0;
int* valPt = &val;

void callback(int* val, FsFile* pr){ // to print out sensorValue in regular interval
  //Serial.println(*val);
  pr->println(*val);
  }

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  t1.begin([=]{callback(valPt, &file);}, 500us); //every 0.5ms print to serial
  t1.start();

  Serial.println("initialization done.");
  Serial.println();

  // Access the built in SD card on Teensy 3.5, 3.6, 4.1 using DMA (maybe faster)
  if (!sd.begin(SD_CONFIG)) {
    sd.initErrorHalt(&Serial);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (sd.exists("saving_test.csv")) {
    sd.remove("saving_test.csv");
  }

  if (!file.open("saving_test.csv", FILE_WRITE)) { // filename needs to be in char
    Serial.println(F("file.open failed"));
    return;
  }
  
  while(Serial.available() == 0){
    val++;
    delay(1);
  }
  file.close();
  
  // List files in SD root.
  sd.ls(LS_DATE | LS_SIZE);
  Serial.println(F("Done"));

  delay(100000);
}
