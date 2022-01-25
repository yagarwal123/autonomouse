#include "check_id_exist.h"

String check_id_exist(String ID, String* KNOWNTAGS,String* TAGNAMES,int noMouse){
  for (int i = 0; i < noMouse; i++) {
      if (KNOWNTAGS[i].compareTo(ID)==0) {
        return TAGNAMES[i];
      };
  }
  return "Mouse does not exist";
}
