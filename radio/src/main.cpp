// What am I doing with my life?
#include <Arduino.h>

#include "config.h"
#include "afsk_avr.h"
#include "afsk_pic32.h"
#include "aprs.h"


void getSerialData();

unsigned long last_sent = 0;
const unsigned long APRS_WAIT = 30000L;

unsigned long last_request = 0;
const unsigned long REQUEST_WAIT = 1000L;

const byte buffer_size = 255;
char buffer[buffer_size];

const char * funk_ready = "FUNK READY";
bool recv_packet = false;


void setup()
{
  Serial.begin(9600);
  afsk_setup();
}

void loop()
{
  if (recv_packet) {
    last_sent = millis();
    aprs_send(buffer);
    while (afsk_flush()) {
    }
    recv_packet = false;
  }
  else {
      if (millis() - last_sent > APRS_WAIT) {
        if (millis() - last_request > REQUEST_WAIT) {
          Serial.println(funk_ready);
          last_request = millis();
        }
        getSerialData();
      }
  }
}


void getSerialData()
{
  static byte ndx = 0;
  char rc;
  while (Serial.available() > 0) {
    rc = Serial.read();
    if (rc != '\n') {
      buffer[ndx++] = rc;
      if (ndx >= buffer_size) {
        ndx = buffer_size - 1;
      }
    } else {
      buffer[ndx] = '\0'; // terminate the string
      ndx = 0;
      recv_packet = true;
    }
  }
}
