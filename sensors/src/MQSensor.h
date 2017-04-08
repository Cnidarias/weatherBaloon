#ifndef __MQSENSOR_H__
#define __MQSENSOR_H__

class MQSensor {
public:
  MQSensor(const int aout, const int dout);
  void setup();
  void read();
  int getLastValue();
  int getLastLimit();

private:
  const int _aout;
  const int _dout;
  int _value;
  int _limit;
};

#endif
