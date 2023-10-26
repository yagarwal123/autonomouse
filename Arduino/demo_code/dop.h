#ifndef dop_h
#define dop_h

//void door_open(Servo door);
void door_open(Servo door, int servonumber);
void door_close(Servo door, bool slower); 
void emergency_door_open_close(Servo door, int servonumber, int open_or_close);

#endif
