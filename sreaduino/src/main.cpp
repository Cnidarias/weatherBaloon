#include <Arduino.h>
#include <SoftwareSerial.h>
#include "MQSensorManager.h"

#include "Ublox.h"
#define SERIAL_BAUD 115200
#define GPS_BAUD 9600
#define N_FLOATS 4
#define UPDATE_DELAY 10000

SoftwareSerial gps_serial(13, 12);
Ublox M8_Gps;
// Altitude - Latitude - Longitude - N Satellites
float gpsArray[N_FLOATS] = {0, 0, 0, 0};

unsigned long delayTimer = 0;

MQSensorManager sensorManager(1);
String getGpsString();


void setup() {
   Serial.begin(SERIAL_BAUD);
   gps_serial.begin(GPS_BAUD);
   sensorManager.add("MQ4", 3, 10);
}

void loop() {
  while(gps_serial.available()){
         char c = gps_serial.read();
         //Serial.print(c);
         if (M8_Gps.encode(c)) {
          gpsArray[0] = M8_Gps.altitude;
          gpsArray[1] = M8_Gps.latitude;
          gpsArray[2] = M8_Gps.longitude;
          gpsArray[3] = M8_Gps.sats_in_use;

          //if (delayTimer < millis()) {
            sensorManager.read();
            String toPrint = sensorManager.getReadString() + getGpsString();
            Serial.println(toPrint);
            //delayTimer = millis() + UPDATE_DELAY;
          //}
        }
  }
}


String getGpsString()
{
  String res = "gps:";
  for(byte i = 0; i < N_FLOATS; i++) {
    res += i == N_FLOATS - 1 ? String(gpsArray[i], 6) : String(gpsArray[i], 6) + ",";
  }
  res += ";";
  return res;
}
