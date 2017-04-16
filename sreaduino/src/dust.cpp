#include "dust.h"

Dust::Dust(const int ledPower, const int measurePin)
  : _ledPower(ledPower)
  , _measurePin(measurePin)
  , _voMeasured(0)
  , _calcVoltage(0)
  , _dustDensity(0)
  {}

void Dust::setup()
{
  pinMode(_ledPower, OUTPUT);
}

void Dust::read()
{
  digitalWrite(_ledPower, LOW);
  delayMicroseconds(_samplingTime);

  _voMeasured = analogRead(_measurePin);

  delayMicroseconds(_deltaTime);
  digitalWrite(_ledPower, HIGH);
  delayMicroseconds(_sleepTime);

  // 0 - 5V mapped to 0-1023 integer values
  // recover voltage

  _calcVoltage = _voMeasured * (5.0 / 1024);

  // linear eqaution taken from http://www.howmuchsnow.com/arduino/airquality/
  // Chris Nafis (c) 2012

  _dustDensity = 0.17 * _calcVoltage - 0.1;
}

String Dust::getReadString()
{
  String res = "Dust r:";
  res += String(_voMeasured);
  res += " v:";
  res += String(_calcVoltage);
  res += " d:";
  res += String(_dustDensity);
  res += ";";
  return res;
}
