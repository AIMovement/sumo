#!/usr/bin/python3

import serial as ser
import re
import argparse as arg
import time
from collections import namedtuple

COMMAND_RANGE = 2**8 - 1

SensorData = namedtuple('SensorData', \
                        'front_left '\
                        'front '\
                        'front_right '\
                        'left '\
                        'right '\
                        'bottom_left '\
                        'bottom_right '\
                        'bottom_back')

class Robot_IO(object):
    def __init__(self, port, baudrate='115200'):
        self._ser = ser.Serial()
        self._ser.port = port
        self._ser.baudrate = baudrate
        self._is_connected = False
        self._s_buf = str()
        self._rx_pattern = re.compile(r"<((\d+,){5}\d+)>", re.MULTILINE)

    def __del__(self):
        self.disconnect()

    def connect(self):
        if not self._is_connected:
            print('Connecting to {0} at baud {1}'.format(self._ser.port, self._ser.baudrate))
            try:
                self._ser.open()
            except ser.SerialException as e:
                print(e)
            else:
                self._is_connected = True
                self._ser.flushInput()
                self._ser.flushOutput()
                self._s_buf = str()

    def disconnect(self):
        if self._is_connected:
            print('Closing serial on device {0}'.format(self._ser.port))
            try:
                self._ser.close()
            except Exception as e:
                print(e)
            else:
                self._is_connected = False

    def send_motor_commands(self, left=0.0, right=0.0):
        assert self._is_connected == True

        left = max(min(left, 1.0), -1.0)
        right = max(min(right, 1.0), -1.0)

        l = int(COMMAND_RANGE*abs(left))
        r = int(COMMAND_RANGE*abs(right))

        header = '<{0}{1}'.format('+' if left >= 0.0 else '-', '+' if right >= 0.0 else '-')
        footer = '>'

        cmd = bytearray(str.encode(header))
        cmd.extend([l,r])
        cmd.extend(str.encode(footer))

        # print("Sending {0}".format(cmd))

        self._ser.write(cmd)

    def is_pending_data(self):
        return self._ser.inWaiting() > 0

    def get_sensors(self):
        assert self._is_connected == True

        n = self._ser.inWaiting()
        if n > 0:
            d = bytearray(self._ser.read(n))
            self._s_buf += d.decode('utf-8')
            matches = tuple(re.finditer(self._rx_pattern, self._s_buf))
            if len(matches) > 0:
                last_match = matches[-1]
                self._s_buf = self._s_buf[last_match.end():]

                values = list(map(int,last_match.group(1).split(',')))

                return SensorData(front_left  = values[0],\
                                  front       = values[1],\
                                  front_right = values[2],\
                                  left        = values[3],\
                                  right       = values[4],\
                                  bottom_left = (values[5] & 0x01 != 0),\
                                  bottom_right= (values[5] & 0x02 != 0),\
                                  bottom_back = (values[5] & 0x04 != 0))

        return None

if __name__ == "__main__":
    print("Test of robot communication using a serial port")

    parser = arg.ArgumentParser()
    parser.add_argument('-p', '--port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('-b', '--baud', default='115200', help='Baudrate')
    parser.add_argument('-w', '--write', help='Command sent to motors, e.g. 0.4,-0.5')
    args = parser.parse_args()

    rio = Robot_IO(args.port, args.baud)

    rio.connect()

    # For some reason, the robot restarts when connecting.
    # Wait for startup, otherwise commands are ignored.
    while not rio.is_pending_data():
        time.sleep(0.1)

    if args.write is not None:
        cmd = list(map(float, args.write.split(',')))
        rio.send_motor_commands(cmd[0], cmd[1])

    else:
        period = 0.02
        while True:
            start_ts = time.time()

            s = rio.get_sensors()
            if s is not None:
                print(s)

            delta = period - (time.time() - start_ts)
            if delta > 0:
                time.sleep(delta)
