#include "Arduino.h"

unsigned start_stimulus(int stimPin, int stimProb){
  unsigned stimulus;
  unsigned noteDuration = 100;
  unsigned noteFrequency;
  int r = random(100);
    if (r < stimProb){
      noteFrequency = 8000;
      stimulus = 1;
    }
    else{
      noteFrequency = 1000;
      stimulus = 0;
    }
    tone(stimPin, noteFrequency, noteDuration);
    return stimulus;
}
