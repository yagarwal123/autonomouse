#include "deliver_reward.h"

//int wait_to_open = 700;// min unit is 7
/*
 * need calibration for the amount of water to be delivered
 * 
 */

void deliver_reward(int rewardPin, int wait_to_open){// wait to open in ms
  digitalWrite(rewardPin, HIGH);
  delay(wait_to_open); // slowly decrease and try
  digitalWrite(rewardPin, LOW);
  //delay(3000); // slowly decrease and try
  }

/*
 delay: 7ms is minimum delay for the valve to work (tested)
 6ms produces clicking sound but is obviously weaker than 7ms
 possibly because the valve do not have time to fully close
*/
