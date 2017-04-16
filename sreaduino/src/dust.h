#ifndef __DUST_H__
#define __DUST_H__

#include <Arduino.h>

class Dust {
public:
  Dust(const int ledPower, const int measurePin);
  void setup();
  void read();
  String getReadString();
private:
  const int _ledPower;
  const int _measurePin;

  float _voMeasured;
  float _calcVoltage;
  float _dustDensity;

  const int _samplingTime = 280;
  const int _deltaTime = 50;
  const int _sleepTime = 9680;
};

#endif
