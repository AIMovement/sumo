/*

ÅF Technology
Robot SM 2015

Template for the ÅF robotic PCB platform

Niklas Cooke
niklas.cooke@afconsult.com

*/

#include <Wire.h>

#include "Sensors.h"


enum {
  LEFT,
  RIGHT
};

enum {
  FORWARD,
  BACKWARD
};


#define AN_BATTERY               A0

#define AN_FR_LEFT_SENSOR        A6
#define AN_FR_MID_SENSOR         A3
#define AN_FR_RIGHT_SENSOR       A2
#define AN_LEFT_SENSOR           A7
#define AN_RIGHT_SENSOR          A1

#define DIG_FR_RIGHT_GROUND_SENSOR  2
#define DIG_FR_LEFT_GROUND_SENSOR   3
#define DIG_FR_BACK_GROUND_SENSOR   7

#define LEFT_MOTORS_FORWARD      5
#define LEFT_MOTORS_BACKWARD     6

#define RIGHT_MOTORS_FORWARD    10
#define RIGHT_MOTORS_BACKWARD    9

#define START                    4
#define STATUS_LED               8

//Macros
#define TOGGLE_STATUS_LED        PORTB ^= 1

bool armed = false;


void setup() {

  Serial.begin(115200);

  Wire.begin();

  initMPU();

  pinMode(AN_FR_LEFT_SENSOR, INPUT);
  pinMode(AN_FR_MID_SENSOR, INPUT);
  pinMode(AN_FR_RIGHT_SENSOR, INPUT);
  pinMode(AN_LEFT_SENSOR, INPUT);
  pinMode(AN_RIGHT_SENSOR, INPUT);

  pinMode(DIG_FR_RIGHT_GROUND_SENSOR, INPUT);
  pinMode(DIG_FR_LEFT_GROUND_SENSOR, INPUT);
  pinMode(DIG_FR_BACK_GROUND_SENSOR, INPUT);
}

void loop() {
  static int initialized = 0;
  int i;

  if (!initialized)
  {
    Serial.println("Send anything to get started!");
    if (Serial.available() > 0)
    {
      Serial.println("Reading some sensor values before starting:");
      for (i=0; i<10; i++)
      {
        readSensors(IR_R | IR_FR | IR_FM | IR_FL | IR_L);
        //readMPU9150();
        delay(20);
      }

      // discard input buffer
      while (Serial.available() > 0)
      {
        Serial.read();
      }

      Serial.println("Initialization done!");
      Serial.println("Send 1-5 for reading IR sensors, with right sensor as 1 and left as 5.");

      initialized = 1;
    }
    else
    {
      return;
    }
  }

  if (Serial.available() > 0) {
    // read the incoming byte:
    int incomingByte = Serial.read();
    unsigned int sensor;

    switch (incomingByte - '0')
    {
      case 1:
        sensor = IR_R;
        break;
      case 2:
        sensor = IR_FR;
        break;
      case 3:
        sensor = IR_FM;
        break;
      case 4:
        sensor = IR_FL;
        break;
      case 5:
        sensor = IR_L;
        break;
      default:
        Serial.println("Invalid request!");
        return;
    }

    for (int i=0; i<2000; i++)
    {
      readSensors(sensor);
      delay(1);
    }
  }
}
