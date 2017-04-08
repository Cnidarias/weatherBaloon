#include "MQSensor.h"
#include <Arduino.h>

MQSensor::MQSensor(const int aout, const int dout)
  : _aout(aout)
  , _dout(dout)
  {}

void MQSensor::setup()
{
  pinMode(_aout, INPUT);
  pinMode(_dout, INPUT);
}

void MQSensor::read()
{
  _value = analogRead(_aout);
  _limit = digitalRead(_aout);
}

int MQSensor::getLastValue()
{
    return _value;
}

int MQSensor::getLastLimit()
{
    return _limit;
}
