  /*****************************************************************************
  Delivers stimulus: sound, odours and visual
  To be modified according to different experiments.
  *****************************************************************************/

#include "Arduino.h"

unsigned start_stimulus(int stimPin[], int oStim[], int nStim, int stimProb, unsigned long stimDuration){
  unsigned stimulus[16]; 
  unsigned noteFrequency;
  int r = random(100);
  int soundProb = stimProb;
  if (r < soundProb){
    //noteFrequency = 8000;
    digitalWrite(stimPin[0], HIGH); // test odour line
    stimulus[0] = 1;
  }
  else{
    //noteFrequency = 1000;
    digitalWrite(stimPin[0], LOW);// test odour line
    stimulus[0] = 0;
  }
  //tone(stimPin[0], noteFrequency, stimDuration);
  delay(stimDuration); // test odour line
  digitalWrite(stimPin[0], LOW); // test odour line

  // olfactory stimulus:

  for(int i=0; i<nStim;i++){ // first element is sound
    digitalWrite(stimPin[i+1], oStim[i]);
    stimulus[i+1] = pStim[i];
    }

  return stimulus; // return an array of stimulus
}


// only for olfactometer
void stop_stimulus(int stimPin[], int nStim){
    for(int i=0; i<nStim;i++){ // first element is sound
    digitalWrite(stimPin[i], LOW);
    }

}