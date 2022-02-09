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

void setup()
{  
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
    
  t1.begin([=]{callback(valPt, &file);}, 1ms, false); //every 0.5ms print to serial
  
//   while (!Serial) {
//    ; // wait for serial port to connect.
//  }

  Serial.print("Initializing SD card...");
    
  // Access the built in SD card on Teensy 3.5, 3.6, 4.1 using DMA (maybe faster)
  if (!sd.begin(SD_CONFIG)) {
    sd.initErrorHalt(&Serial);
  }
 
  Serial.println("card initialized.");
}

void loop()
{
  if (sd.exists("saving_test.csv")) {
    sd.remove("saving_test.csv");
  }
  
  if (!file.open("saving_test.csv", FILE_WRITE)) { // filename needs to be in char
    Serial.println(F("file.open failed"));
    return;
  }
  Serial.println("saving data");
  t1.start();
  while(Serial.available() == 0){
    val++;
    //Serial.println(val);
    delay(1);
  }
  t1.stop();
  file.close();
  
  // List files in SD root.
  sd.ls(LS_DATE | LS_SIZE);
  Serial.println(F("Done writing"));

  Serial.println("dumping file...");

  if (!file.open("saving_test.csv", FILE_WRITE)) { // filename needs to be in char
    Serial.println(F("file.open failed"));
    return;
  }
  
  file.rewind();
  //dump_file("saving_test.csv", &file);

  while(file.available()){ // file is available
    char line[40];
    int data = file.fgets(line, sizeof(line));
    Serial.println(line);
  }

/*
    char line[40];
    while (file.available()) {
    int n = file.fgets(line, sizeof(line));
    if (n <= 0) {
      error("fgets failed");
    }
    if (line[n-1] != '\n' && n == (sizeof(line) - 1)) {
      error("line too long");
    }
    if (!parseLine(line)) {
      error("parseLine failed");
    }
    Serial.println(line);
  }
*/
/*
  while (file.available()){
    int data;
    int n = fread(data, sizeof(data), 1);
    Serial.println(data);
    }
    */
  file.close();
  Serial.println("finished dumping");

  // List files in SD root.
  sd.ls(LS_DATE | LS_SIZE);

  delay(1000000);
}
