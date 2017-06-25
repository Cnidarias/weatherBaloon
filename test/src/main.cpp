#include <Arduino.h>

void setup()
{
  pinMode(2, OUTPUT);
}
bool status = false;
void loop()
{
    if (status)
     digitalWrite(2, HIGH);

    else
      digitalWrite(2, LOW);
    status = !status;
    delay(10000);
}
