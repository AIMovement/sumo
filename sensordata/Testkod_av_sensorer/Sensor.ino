#include "Sensors.h"

volatile int FLsensor;
volatile int FMsensor;
volatile int FRsensor;
volatile int Lsensor;
volatile int Rsensor;

volatile int FRdig;
volatile int FLdig;
volatile int Bdig;

void readSensors(unsigned int sensors) {

  if (sensors & IR_FL)
  {
    FLsensor = analogRead(AN_FR_LEFT_SENSOR);
    Serial.print("FL = ");
    Serial.println(FLsensor);
  }

  if (sensors & IR_FM)
  {
    FMsensor = analogRead(AN_FR_MID_SENSOR);
    Serial.print("FM = ");
    Serial.println(FMsensor);
  }

  if (sensors & IR_FR)
  {
    FRsensor = analogRead(AN_FR_RIGHT_SENSOR);
    Serial.print("FR = ");
    Serial.println(FRsensor);
  }

  if (sensors & IR_L)
  {
    Lsensor = analogRead(AN_LEFT_SENSOR);
    Serial.print("L = ");
    Serial.println(Lsensor);
  }

  if (sensors & IR_R)
  {
    Rsensor = analogRead(AN_RIGHT_SENSOR);
    Serial.print("R = ");
    Serial.println(Rsensor);
  }

//  FRdig = digitalRead(DIG_FR_RIGHT_GROUND_SENSOR);
//  FLdig = digitalRead(DIG_FR_LEFT_GROUND_SENSOR);
//  Bdig = digitalRead(DIG_FR_BACK_GROUND_SENSOR);

//  Serial.println(FRdig);
//  Serial.println(FLdig);
//  Serial.println(Bdig);
}
