// What am I doing with my life?
#include <Arduino.h>

#include "config.h"
#include "afsk_avr.h"
#include "afsk_pic32.h"
#include "aprs.h"

// #define DEBUG_AX25 1

const char * str = "test\0";
const char * str2 = "another test is something";

void setup()
{
  Serial.begin(9600);
  Serial.print("start");
  afsk_setup();
}
bool state = false;

void loop()
{
  if (state) aprs_send(str);
  else aprs_send(str2);

  state = !state;

  delay(10000);
}
