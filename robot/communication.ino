#include "communication.h"

static void reset(parser_t *p)
{
  p->state = WAITING;
  p->timeout = 0;
}

int get_motor_command(parser_t *p, motor_cmd_t *complete_cmd)
{
  /*
     A command could look like:
       "<+-ab>"
     Meaning 
       left  = forward  (+) 97 ('a')
       right = backward (-) 98 ('b')
   */

  int nof_avail = Serial.available();
  int is_complete = 0;

  if (nof_avail > CMD_LEN) {
    nof_avail = CMD_LEN;
  }
  
  if (0 == nof_avail) {
    p->timeout++;
  } else {
    p->timeout = 0;
  }

  if (p->timeout >= TIMEOUT) {
    reset(p);
  }

  for (int i = 0; i < nof_avail; i++) {
    const char b = Serial.read();

    switch (p->state) {
      case WAITING:
        if ('<' == b) {
	        p->state = LEFT_DIR;
	      }
	      break;

      case LEFT_DIR:
        p->buf.left_dir = ('+' == b) ? FORWARD : BACKWARD;
        p->state = RIGHT_DIR;
        break;

      case RIGHT_DIR:
        p->buf.right_dir = ('+' == b) ? FORWARD : BACKWARD;
        p->state = LEFT_VAL;
	      break;

      case LEFT_VAL:
        p->buf.left_command = b;
	      p->state = RIGHT_VAL;
        break;

      case RIGHT_VAL:
        p->buf.right_command = b;
	      p->state = FOOTER;
	      break;

      case FOOTER:
	      is_complete = ('>' == b);
        if (is_complete) {
	        *complete_cmd = p->buf;
	      }
	      reset(p);
	      break;
      
      default:
	      reset(p);
        break;
    }
  }

  return is_complete;
}

void send_sensor_data(sensor_data_t data)
{
  Serial.print('<');
  for (int i = 0; i < NOF_DISTANCE_SENSORS; i++) {
    Serial.print(data.distance[i]);
    Serial.print(',');
  }
  Serial.print(data.ground);
  Serial.println('>');
}
