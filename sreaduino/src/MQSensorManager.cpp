#include "MQSensorManager.h"
#include "MQSensor.h"
#include <Arduino.h>

MQSensorManager::MQSensorManager(const int how_many)
  : _how_many(how_many)
  , _addingIndex(0)
  {
    _namedSensors = new NamedMQSensor[_how_many];
  }

  void MQSensorManager::add(const char * name, const int aout, const int dout)
  {
      if (_addingIndex >= _how_many) return;
      _namedSensors[_addingIndex].sensor = new MQSensor(aout, dout);
      _namedSensors[_addingIndex].sensor->setup();
      _namedSensors[_addingIndex].name = name;
      _addingIndex++;
  }

  void MQSensorManager::read()
  {
    for (int i = 0; i < _how_many; i++)
      _namedSensors[i].sensor->read();
  }

  String MQSensorManager::getReadString()
  {
    String res = "";
    res += " ";
    for (int i = 0; i < _how_many; i++) {
      res += _namedSensors[i].name;
      res += " v:";
      res += String(_namedSensors[i].sensor->getLastValue());
      // res += " l:";
      // res += String(_namedSensors[i].sensor->getLastLimit());
      res += ";";
    }
    return res;
  }
