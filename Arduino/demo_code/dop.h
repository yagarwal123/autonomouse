#ifndef dop_h
#define dop_h

void door_open(Servo door);
void door_close(Servo door); 
//void door_open(Servo door);
void door_open(Servo door, int servonumber);
void door_close(Servo door, bool slower); 

#endif