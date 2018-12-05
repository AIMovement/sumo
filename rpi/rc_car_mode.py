#!/usr/bin/python3

from robot_communication import Robot_IO
import pyglet
from pyglet.window import key
import time

class Control(object):

    def __init__(self, rio, print_sensors=False):
        super(Control, self).__init__()

        self.rio = rio
                
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.win = pyglet.window.Window()
        self.win.push_handlers(self.keyboard)

        self.rio.connect()

        while not self.rio.is_pending_data():
            time.sleep(0.10)

        self.cmd = (0.0, 0.0)
        
        pyglet.clock.schedule_interval(self.motor_update, 0.05)

        if print_sensors:
            pyglet.clock.schedule_interval(self.sensor_update, 0.2)

    def sensor_update(self, dt):
        s = rio.get_sensors()
        if s is not None:
            print(s)

    def is_pressed(self, k):
        return self.keyboard[k]

    def motor_update(self, dt):
        if self.is_pressed(key.Q):
            self.rio.disconnect()
            quit()

        elif self.is_pressed(key.UP):
            if self.is_pressed(key.LEFT):
                cmd = (0.5, 1.0)
            elif self.is_pressed(key.RIGHT):
                cmd = (1.0, 0.5)
            elif self.is_pressed(key.DOWN):
                cmd = (0.0, 0.0)
            else:
                cmd = (1.0, 1.0)

        elif self.is_pressed(key.LEFT):
            if self.is_pressed(key.DOWN):
                cmd = (-0.5, -1.0)
            elif self.is_pressed(key.RIGHT):
                cmd = (0.0, 0.0)
            else:
                cmd = (-0.5, 0.5)

        elif self.is_pressed(key.RIGHT):
            if self.is_pressed(key.DOWN):
                cmd = (-1.0, -0.5)
            else:
                cmd = (0.5, -0.5)

        elif self.is_pressed(key.DOWN):
            cmd = (-1.0, -1.0)

        else:
            cmd = (0.0, 0.0)

        scale = 0.5
        cmd = (scale*cmd[0], scale*cmd[1])

        if cmd != self.cmd:
            self.send(cmd)
            self.cmd = cmd
        
    def send(self, cmd):
        self.rio.send_motor_commands(cmd[0], cmd[1])

if __name__ == "__main__":
    print("Use the arrow keys to control the robot")
    
    rio = Robot_IO('/dev/ttyUSB0', '115200')

    ctrl = Control(rio)
    
    pyglet.app.run()
