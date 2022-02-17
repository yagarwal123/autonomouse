#ifndef time_functions_h
#define time_functions_h
#include <Arduino.h>  //For string type

void dateTime(uint16_t* date, uint16_t* time, uint8_t* ms10);
void printField(Print* pr, char sep, uint8_t v);
void printNow(Print* pr);

#endif
