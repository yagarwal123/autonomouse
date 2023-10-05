  /*****************************************************************************
  Standard time and date function for book keeping
  *****************************************************************************/


#include <TimeLib.h>
#include "time_functions.h"
#include "SdFat.h"

void dateTime(uint16_t* date, uint16_t* time, uint8_t* ms10) {
  
  // Return date using FS_DATE macro to format fields.
  *date = FS_DATE(year(), month(), day());

  // Return time using FS_TIME macro to format fields.
  *time = FS_TIME(hour(), minute(), second());
  
  // Return low time bits in units of 10 ms.
  *ms10 = second() & 1 ? 100 : 0;
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
