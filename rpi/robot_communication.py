import serial as ser
import argparse as arg
import time

COMMAND_RANGE = 2**8 - 1

class Robot_IO(object):
    def __init__(self, port, baudrate='115200'):
        self._ser = ser.Serial()
        self._ser.port = port
        self._ser.baudrate = baudrate
        self._is_connected = False

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

    def disconnect(self):
        if self._is_connected:
            print('Closing serial on device {0}'.format(self._ser.port))
            try:
                self._ser.close()
            except serial.SerialException as e:
                print(e)
            else:
                self._is_connected = False
        
        self._ser.close()

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
        
        print("Sending {0}".format(cmd))

        self._ser.write(cmd)

    def get_sensors_blocking(self, timeout_s):
        self._ser.timeout = timeout_s
        return self._ser.read(100)
    
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
    time.sleep(5.0)

    if args.write is not None:
        cmd = list(map(float, args.write.split(',')))
        rio.send_motor_commands(cmd[0], cmd[1])

    else:
        print("Read!")
