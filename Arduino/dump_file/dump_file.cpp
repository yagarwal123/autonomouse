#include "dump_file.h"
#include <SD.h>

bool dump_file(char fileName){
  
  // open the file.
  File dataFile = SD.open(fileName);

  // if the file is available, write to serial:
  if (dataFile) {
    while (dataFile.available()) {
      Serial.write(dataFile.read());
    }
    dataFile.close();
  }  
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
    return 0;
  } 
  
  return 1;
}
