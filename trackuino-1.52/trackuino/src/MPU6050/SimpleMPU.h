#ifndef __SIMPLEMPU_H__
#define __SIMPLEMPU_H__

#include "I2C/I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

extern volatile bool mpuInterrupt;
extern uint16_t fifoCount;
extern uint16_t packetSize;

void mpu_setup();
void mpu_loop();

#endif
