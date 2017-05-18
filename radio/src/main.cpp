// What am I doing with my life?
#include <Arduino.h>

#include "config.h"
#include "afsk_avr.h"
#include "afsk_pic32.h"
#include "aprs.h"

void setup()
{
  aprs_send("this is a test");
}

void loop()
{

}
