// What am I doing with my life?
#include <Arduino.h>

#include "config.h"
#include "afsk_avr.h"
#include "afsk_pic32.h"
#include "aprs.h"

// #define DEBUG_AX25 1

const char * str = "this is a long string it should be llonger blah blah blah blah blah blah blahlonger blah blah blah blah blah blah blahlonger blah blah blah blah blah blah blahonger blah blah blah blah blah blah blah\0";

void setup()
{
  Serial.begin(9600);
  Serial.print("start");
}

void loop()
{
  aprs_send(str);
  delay(10000);
}
