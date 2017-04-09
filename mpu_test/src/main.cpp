#include <Arduino.h>

#include "MPU6050/SimpleMPU.h"

void setup()
{
  mpu_setup();
}

void loop()
{
  while (mpu_check_interupt()) {

  }
  mpu_loop();
}
