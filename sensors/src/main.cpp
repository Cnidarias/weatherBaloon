#include <Arduino.h>
#include <Servo.h>

#include "MQSensorManager.h"
#include "dust.h"

unsigned long sensor_lasttime = 0;
unsigned long servor_lasttime = 0;

boolean cycleCheck(unsigned long *lastMillis, unsigned int cycle)
{
  unsigned long currentMillis = millis();
  if(currentMillis - *lastMillis >= cycle)
  {
    *lastMillis = currentMillis;
    return true;
  }
  else
  return false;
}

MQSensorManager manager(4);
Dust dust(20, 30);

Servo servo;

int servo_dest_angle = 360;
int servo_angle = 0;


void setup() {
  Serial.begin(9600);
  manager.add("MQ3", 0, 36);
  manager.add("MQ131", 1, 35);
  manager.add("MQ4", 2, 34);
  manager.add("MQ135", 3, 33);

  dust.setup();

  servo.attach(7);
  servo.write(0);
  delay(5000);
}

void loop() {
  if (cycleCheck(&sensor_lasttime, 100)) {
    manager.read();
    dust.read();
    Serial.println(String(millis()) + " " + manager.getReadString() + dust.getReadString());
  }

  if (cycleCheck(&servor_lasttime, 5)) {
      if (servo_angle < servo_dest_angle) {
        servo_angle++;
        if (servo_angle <= 180)
          servo.write(servo_angle);
        else
          servo.write(180 - (servo_angle - 180));
      } else {
        servo_angle = 0;
      }
  }
}
