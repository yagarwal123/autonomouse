#include "read_id.h"

boolean check_tag_valid(char* newTag){

  if ((newTag[10] == '\r')){
    return true;
  }
  else {return false;};
}

String read_id(HardwareSerial &refSer){
  /*
    read until the first 13, then read the next 11 chars
    tag is valid when the 11th char is 13 (\r)
    return tag if tag is valid, else retun empty
  */
  
  if (refSer.available()) { 
    char newTag[11];
    Serial.println("Serial available");
    int i = 0;
    int read_byte;
    read_byte = refSer.read();
    //Serial.println(read_byte);
    while (read_byte != 13){
      //Serial.println("Reached here 1");
      while (!refSer.available()){}; // wait until serial buffer is not empty
      read_byte = refSer.read();//Serial.println(read_byte);
    };//reach the first end of seq
    //Serial.println("Reached here 2");
    unsigned long strt_time = millis();
    while ( (i < 11) && ( (millis() - strt_time) < 1000) ) {
      while (refSer.available()){ // better performance
        read_byte = refSer.read();
        //Serial.println(read_byte);
        newTag[i] = read_byte;
        i++;
      }
    }
    //Serial.println("Reached here 3");
    if (check_tag_valid(newTag)){
      String finalTag = newTag;
      finalTag.trim();
      return finalTag;
      }
    else {return "";};
  }
  else {return "";};
}


  
 
