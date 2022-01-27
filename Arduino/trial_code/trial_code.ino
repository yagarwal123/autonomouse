#include "SdFat.h"
#include <TimeLib.h>
#include "run_test.h"

// for SD card access--------------------------
#define SD_FAT_TYPE 3/*
#ifndef SDCARD_SS_PIN
const uint8_t SD_CS_PIN = SS;
#else  // SDCARD_SS_PIN
// Assume built-in SD is used.
const uint8_t SD_CS_PIN = SDCARD_SS_PIN;
#endif  // SDCARD_SS_PIN
*/
// Try to select the best SD card configuration.
//#if HAS_SDIO_CLASS
#define SD_CONFIG SdioConfig(FIFO_SDIO)
//#elif ENABLE_DEDICATED_SPI
//#define SD_CONFIG SdSpiConfig(SD_CS_PIN, DEDICATED_SPI)
//#else  // HAS_SDIO_CLASS
//#define SD_CONFIG SdSpiConfig(SD_CS_PIN, SHARED_SPI)
//#endif  // HAS_SDIO_CLASS

/*
#if SD_FAT_TYPE == 0
SdFat sd;
File file;
#elif SD_FAT_TYPE == 1
SdFat32 sd;
File32 file;
#elif SD_FAT_TYPE == 2
SdExFat sd;
ExFile file;
#elif SD_FAT_TYPE == 3
SdFs sd;
FsFile file;
#else  // SD_FAT_TYPE
#error Invalid SD_FAT_TYPE
#endif  // SD_FAT_TYPE*/
SdFs sd;
FsFile file;
//------------------------------------------------------------------------------
// Call back for file timestamps.  Only called for file create and sync().
void dateTime(uint16_t* date, uint16_t* time, uint8_t* ms10) {
  
  // Return date using FS_DATE macro to format fields.
  *date = FS_DATE(year(), month(), day());

  // Return time using FS_TIME macro to format fields.
  *time = FS_TIME(hour(), minute(), second());
  
  // Return low time bits in units of 10 ms.
  *ms10 = second() & 1 ? 100 : 0;
}
//------------------------------------------------------------------------------
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


// Variables for the lick and reward system
int rewardPin = 32;
int lickPin = A13;
int THRESHOLD = 100;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(rewardPin, OUTPUT);
  digitalWrite(rewardPin, LOW);
  
  // set the Time library to use Teensy 3.0's RTC to keep time
  setSyncProvider(getTeensy3Time);

  if (timeStatus()!= timeSet) {
  Serial.println("Unable to sync with the RTC");
  return;
  }

  Serial.print(F("DateTime::now "));
  printNow(&Serial);
  Serial.println();
  // Set callback
  FsDateTime::setCallback(dateTime);

  // Access the built in SD card on Teensy 3.5, 3.6, 4.1 using DMA (maybe faster)
  if (!sd.begin(SD_CONFIG)) {
    sd.initErrorHalt(&Serial);
  }
  Serial.println("initialization done.");
  Serial.println();
  
} 

void loop() {
  String ID = "stuart";
  // put your main code here, to run repeatedly:

  // create file name with ID and time
  String fileName = ID + month()+"_"+day()+"_"+hour()+"_"+minute()+"_"+second()+".txt";
  Serial.println(fileName);
  char buf[30];
  fileName.toCharArray(buf, 30);
  Serial.println(buf);
  
  // Remove old version to set create time.
  if (sd.exists(fileName)) {
    sd.remove(fileName);
  }

  if (!file.open(buf, FILE_WRITE)) { // filename needs to be in char
    Serial.println(F("file.open failed"));
    return;
  }
  
  // Print current date time to file.
  file.print(F("Test file at: "));
  printNow(&file);
  file.println();
  file.print(F("time(ms), ")); // print headings
  file.println(F("amplitude"));
  
  int liquidAmount = 500; // command from raspi
  run_test(lickPin, THRESHOLD, rewardPin, liquidAmount, &file); // write to file during test

  file.close(); // close the file
  
  // List files in SD root.
  sd.ls(LS_DATE | LS_SIZE);
  Serial.println(F("Done"));

  delay(100000);
}
