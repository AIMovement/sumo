import numpy as np
import math

class Sumobot(object):

    def __init__(self, x0, y0):
        self.pos = np.array([x0, y0])
        self.angle = 0.0

        self.size = 0.10
        self.wheel_radius = 0.015

    def step(self, dt, rot_vel_wheel_left, rot_vel_wheel_right):
        # Model inspiration from
        # http://kdm.p.lodz.pl/articles/2011/15_4_5.pdf

        vl = rot_vel_wheel_left  * self.wheel_radius
        vr = rot_vel_wheel_right * self.wheel_radius

        beta_dot = (vr - vl)/self.size

        self.angle += beta_dot * dt

        avg_vel = (vl + vr)/2.0

        x_dot = avg_vel * math.cos(self.angle)
        y_dot = avg_vel * math.sin(self.angle)

        self.pos += np.array([x_dot, y_dot]) * dt

    def state(self):
        return np.array([self.pos[0], self.pos[1], self.angle])