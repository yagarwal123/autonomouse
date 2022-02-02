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
    Serial.println("Mouse detected");
    int i = 0;
    int read_byte;
    read_byte = refSer.read();
    //Serial.println(read_byte);
    while (read_byte != 13){
      while (!refSer.available()){}; // wait until serial buffer is not empty
      read_byte = refSer.read();//Serial.println(read_byte);
    };//reach the first end of seq
    while (i < 11) {
      while (!refSer.available()){}; // better performance
      read_byte = refSer.read();
      //Serial.println(read_byte);
      newTag[i] = read_byte;
      i++;
    }
    if (check_tag_valid(newTag)){
      String finalTag = newTag;
      finalTag.trim();
      return finalTag;
      }
    else {return "";};
  }
  else {return "";};
}


  
 
