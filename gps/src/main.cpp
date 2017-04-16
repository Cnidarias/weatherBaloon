#include <Arduino.h>
#include <SoftwareSerial.h>

#include "Ublox.h"
#define SERIAL_BAUD 115200
#define GPS_BAUD 115200
#define N_FLOATS 4

SoftwareSerial gps_serial(13, 12);
Ublox M8_Gps;
// Altitude - Latitude - Longitude - N Satellites
float gpsArray[N_FLOATS] = {0, 0, 0, 0};

void setup() {
   Serial.begin(SERIAL_BAUD);
   gps_serial.begin(9600);
}

void loop() {
   if(!gps_serial.available()) {

		return;
   }
  while(gps_serial.available()){
         char c = gps_serial.read();
         Serial.println(c);
         if (M8_Gps.encode(c)) {
          gpsArray[0] = M8_Gps.altitude;
          gpsArray[1] = M8_Gps.latitude;
          gpsArray[2] = M8_Gps.longitude;
          gpsArray[3] = M8_Gps.sats_in_use;
        }
  }
  for(byte i = 0; i < N_FLOATS; i++) {
    Serial.print(gpsArray[i], 6);Serial.print(" ");
  }
  Serial.println("");
}
