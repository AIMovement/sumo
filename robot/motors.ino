#include "motors.h"

void set_motors(motor_cmd_t cmd)
{
  switch (cmd.left_dir) {
    case FORWARD:
      analogWrite(LEFT_MOTORS_BACKWARD, 0);
      analogWrite(LEFT_MOTORS_FORWARD, cmd.left_command);
      break;

    case BACKWARD:
      analogWrite(LEFT_MOTORS_FORWARD, 0);
      analogWrite(LEFT_MOTORS_BACKWARD, cmd.left_command);
      break;

    default:
      analogWrite(LEFT_MOTORS_FORWARD, 0);
      analogWrite(LEFT_MOTORS_BACKWARD, 0);
      break;
  }
  
  switch (cmd.right_dir) {
    case FORWARD:
      analogWrite(RIGHT_MOTORS_BACKWARD, 0);
      analogWrite(RIGHT_MOTORS_FORWARD, cmd.right_command);
      break;

    case BACKWARD:
      analogWrite(RIGHT_MOTORS_FORWARD, 0);
      analogWrite(RIGHT_MOTORS_BACKWARD, cmd.right_command);
      break;

    default:
      analogWrite(RIGHT_MOTORS_FORWARD, 0);
      analogWrite(RIGHT_MOTORS_BACKWARD, 0);
      break;
  }
}
