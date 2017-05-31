#include <Arduino.h>

void setup()
{
  pinMode(3, OUTPUT);
}
bool status = false;
void loop()
{
    if (status)
     digitalWrite(3, HIGH);

    else
      digitalWrite(3, LOW);
    status = !status;
    delay(100);
}
