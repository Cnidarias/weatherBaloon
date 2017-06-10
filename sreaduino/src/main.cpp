#include <Arduino.h>
#include <SoftwareSerial.h>
#include "MQSensorManager.h"
#include "dust.h"

#include "Ublox.h"
#define SERIAL_BAUD 9600
#define GPS_BAUD 9600
#define N_FLOATS 4
#define UPDATE_DELAY 10000

void readGps();

SoftwareSerial gps_serial(12, 13);
Ublox M8_Gps;
// Altitude - Latitude - Longitude - N Satellites
float gpsArray[N_FLOATS] = {0, 0, 0, 0};

unsigned long delayTimer = 0;

MQSensorManager sensorManager(5);
String getGpsString();
Dust dust(8, 6);

unsigned long last_sensor_read = 0;
const unsigned long SENSOR_DELAY = 1000L;

void setup() {
  Serial.begin(SERIAL_BAUD);
  gps_serial.begin(GPS_BAUD);
  sensorManager.add("3", 8, 10);
  sensorManager.add("7", 9, 10);
  sensorManager.add("4", 10, 10);
  sensorManager.add("135", 11, 10);
  sensorManager.add("131", 12, 10);
}

void loop() {
  if (millis() - last_sensor_read > SENSOR_DELAY) {
    sensorManager.read();
    dust.read();

    String toPrint = getGpsString() + sensorManager.getReadString() + dust.getReadString();
    Serial.println(toPrint);
    last_sensor_read = millis();
  }

  readGps();
}

void readGps()
{
  while(gps_serial.available()){
    char c = gps_serial.read();
    if (M8_Gps.encode(c)) {
      gpsArray[0] = M8_Gps.altitude;
      gpsArray[1] = M8_Gps.latitude;
      gpsArray[2] = M8_Gps.longitude;
      gpsArray[3] = M8_Gps.sats_in_use;
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
