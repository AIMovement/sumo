#ifndef _COMMUNICATION_H
#define _COMMUNICATION_H

#include "motors.h"

#define TIMEOUT (2000)
#define CMD_LEN (6)

enum {
  WAITING,
  LEFT_DIR,
  RIGHT_DIR,
  LEFT_VAL,
  RIGHT_VAL,
  FOOTER
};

typedef struct {
  char state = WAITING;
  int  timeout = 0;
  motor_cmd_t buf;
} parser_t;

#define NOF_DISTANCE_SENSORS (5)
#define FRONT_LEFT_DIG (1)
#define FRONT_RIGHT_DIG (1 << 1)
#define BACK_DIG (1 << 2)

typedef int distance_sensors_t[NOF_DISTANCE_SENSORS];
typedef unsigned int ground_sensor_t;

typedef struct {
  distance_sensors_t distance;
  ground_sensor_t ground;
} sensor_data_t;

int get_motor_command(parser_t *p, motor_cmd_t *complete_cmd);
void send_sensor_data(sensor_data_t data);

#endif
