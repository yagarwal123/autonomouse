#include "clear_serial_buffer.h"

// takes in serial port and clears the buffer

void clear_serial_buffer(HardwareSerial &refSer){
  int temp;
  while (refSer.available() > 0) { 
    temp = refSer.read();
  }//read the rest of the input buffer until empty
}
