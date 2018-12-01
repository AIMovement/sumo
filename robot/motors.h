#ifndef _MOTORS_H
#define _MOTORS_H

enum {
  LEFT_MOTOR,
  RIGHT_MOTOR
};

enum {
  FORWARD,
  BACKWARD
};

typedef struct {
  unsigned char left_command = 0;
  char left_dir = FORWARD;
  unsigned char right_command = 0;
  char right_dir = FORWARD;
} motor_cmd_t;

void set_motor(motor_cmd_t cmd);

#endif
