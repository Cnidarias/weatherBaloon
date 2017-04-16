
#ifndef __MQSENSORMANAGER_H__
#define __MQSENSORMANAGER_H__

#include "MQSensor.h"
#include "Arduino.h"

struct NamedMQSensor {
  MQSensor * sensor;
  const char * name;
};


class MQSensorManager {
public:
  MQSensorManager(const int how_many);
  void add(const char * name, const int aout, const int dout);
  void read();
  String getReadString();

private:
  NamedMQSensor * _namedSensors;
  int _how_many;
  int _addingIndex;
};

#endif
