#include "sensors.h"
#include "communication.h"

static char read_ground_sensors(void)
{
  ground_sensor_t tmp = 0;
  tmp |= (digitalRead(DIG_FR_LEFT_GROUND_SENSOR) ? FRONT_LEFT_DIG : 0);
  tmp |= (digitalRead(DIG_FR_RIGHT_GROUND_SENSOR) ? FRONT_RIGHT_DIG : 0);
  tmp |= (digitalRead(DIG_FR_BACK_GROUND_SENSOR) ? BACK_DIG : 0);
  return tmp;
}

static void read_distance_sensors(distance_sensors_t data)
{
  data[0] = analogRead(AN_FR_LEFT_SENSOR);
  data[1] = analogRead(AN_FR_MID_SENSOR);
  data[2] = analogRead(AN_FR_RIGHT_SENSOR);
  data[3] = analogRead(AN_LEFT_SENSOR);
  data[4] = analogRead(AN_RIGHT_SENSOR);
}

void read_sensors(sensor_data_t *data)
{
  read_distance_sensors(data->distance);
  data->ground = read_ground_sensors();
}
