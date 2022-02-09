#include <SD.h>
#include <SPI.h>
#include "dump_file.h"

const int chipSelect = BUILTIN_SDCARD;

void setup()
{  
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
   while (!Serial) {
    ; // wait for serial port to connect.
  }

  Serial.print("Initializing SD card...");
  
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");
  
  dump_file("test.csv");
}

void loop()
{
}
