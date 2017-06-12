// What am I doing with my life?
#include <Arduino.h>

#include "config.h"
#include "afsk_avr.h"
#include "afsk_pic32.h"
#include "aprs.h"


void getSerialData();

unsigned long last_sent = 0;
const unsigned long APRS_WAIT = 10000L;

unsigned long last_request = 0;
const unsigned long REQUEST_WAIT = 5000L;

const byte buffer_size = 255;
char buffer[buffer_size];

const char * funk_ready = "FUNK READY";
bool recv_packet = false;

const char * strs[]= {
  "/175722h5021.41N/00735.34EO/A=65.61\0",
  "{0_0_d+sW4Acc!cnx5FQAAABAEABtin.hIA3nHj2K,W2Z$Y@!FH8_7PRVc%/.U!!06!.AMlWZ1RIGv#}KN7*#H8$Y%~qf\"^]~B\"!T7}B\"~]*>Z~d+tWwA5WuWYBDHRtIAKcNtMA@QRtlBAAAAAAAAAAAAAA6\0",
  "{0_1_Fa\"*BFO0WjLXLhtUE[hFBIO{WAAAAAAS\"|LdL;y[FKOGM[wU*XjqI6DZYgSUSTz71w)@9NA&ABA+>J\"_zqNx2Ezze0D$[]iBMR$vGLGgjCYr7Ky!M5d/GB5Od&g/t.Z%Qy/9MmKucKG7j10>`7nCSy=\0",
  "{0_2_|vs$qA}_Bz5x!<IacYjzlc?5dw{wXh1l[1v4|G>lnK[Go[|ECdb@+8!u=5tG>J4wCb?XB5]F7i3Xlt+I;11.Oa|,IaX7MM06NMQHFPp7JRVb4!SC8%P3)Wvak:#]L7%;=[])I)<q(lw87ICZL!U/@q)\0"
};

bool test_strings = true;

void setup()
{
  Serial.begin(9600);
  afsk_setup();
}

void loop()
{
  if (test_strings) {
    int i = 0;
    for (; i < 4; i++)  {
      aprs_send(strs[i]);
      Serial.println(strs[i]);
      while (afsk_flush()) {}
      delay(15000);
    }
    delay(15000);
  }
  else {
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
