#include "FIR.h"
/*
MAF algorithm adopted from
https://nestedsoftware.com/2018/03/20/calculating-a-moving-average-on-streaming-data-5a7k.22879.html
*/

//define the variable in the stack memory, including declaration. The value of this
//FIR_FILTER_IMPULSE_RESPONSE array is based on a design (the value represent the behaviour of the filter)
//static float FIR_FILTER_IMPULSE_RESPONSE[FIR_FILTER_LENGTH]={0.4,0.3,0.2,0.1,0.05}; 

//function to initialise the circular buffer value
void FIRFilter_init(FIRFilter *fir){ //use pointer to FIRFilter variable so that we do not need to copy the memory value (more efficient)
  //clear the buffer of the filter
  for(int i=0;i<FIR_FILTER_LENGTH;i++){
      fir->buff[i]=0;
  }
  //Reset the buffer index
  fir->buffIndex=0;
  //clear filter output
  fir->out=0;
}

//function to calculate (process) the filter output
float FIRFilter_calc(FIRFilter *fir, float inputVal){
    /*Implementing CIRCULAR BUFER*/
    // store the old sample value in variable
    float  old = fir->buff[fir->buffIndex];
    //Store the latest sample=inputVal into the circular buffer
    fir->buff[fir->buffIndex]=inputVal;
    
    //Increase the buffer index. return to zero if it reach the end of the index (circular buffer)
    fir->buffIndex++;
    if(fir->buffIndex==FIR_FILTER_LENGTH){
        fir->buffIndex=0;
    }

    //Compute the filtered sample with moving average filter
    if(old < 1){
        return inputVal; // return input value when the buffer is not full
    }
    else{
        fir->out = fir->out + ((inputVal - old)/FIR_FILTER_LENGTH); // out + (new-old)/window
        //return the filtered data
        return fir->out;
    }
}
