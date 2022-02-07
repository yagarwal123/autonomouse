#ifndef FIR_FILTER_H
#define FIR_FILTER_H

/*
The directives are used to avoid double declaration of data types, 
functions or other included libraries. 
This practice is recommended for C/C++ header files.
*/

/*
Adopted from 
https://www.wasyresearch.com/tutorial-c-c-implementation-of-circular-buffer-for-fir-filter-and-gnu-plotting-on-linux/
*/

#include <stdint.h>

#define FIR_FILTER_LENGTH 10

//Defining the struct to represent the circular buffer
typedef struct{
  float buff[FIR_FILTER_LENGTH]; //for circular buffer array
  uint8_t buffIndex; //Tracking the index of the circular buffer
  float out; //the output value of the circular buffer
} FIRFilter;

//functions prototype
void FIRFilter_init(FIRFilter *fir);
float FIRFilter_calc(FIRFilter *fir, float inputVal);

#endif
