#ifndef SENSORS_H
#define SENSORS_H

typedef enum
{
  IR_R  = 0x01,
  IR_FR = 0x02,
  IR_FM = 0x04,
  IR_FL = 0x08,
  IR_L  = 0x10
} IR_sensor;

void readSensors(unsigned int sensors);

#endif
