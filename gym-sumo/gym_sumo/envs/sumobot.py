import numpy as np
import math

class DistanceSensor(object):
    def __init__(self, robot, pos, angle):
        self.robot = robot

    def value(self):
        return 10.0

class DigitalSensor(object):
    def __init__(self, robot, pos):
        self.robot = robot

    def value(self):
        return False

def rotate(vec, angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.matrix([[c,-s], [s, c]]) * vec

class Sumobot(object):

    def __init__(self, arena, x0, y0, angle0=0.0):
        self.arena = arena
        self.pos = np.matrix([[x0], [y0]])
        self.angle = angle0

        self.rot_vel_wheel_right = 0.0
        self.rot_vel_wheel_left = 0.0

        self.size = 0.10
        self.wheel_radius = 0.015

        self.distance_sensors = [
            DistanceSensor(self, pos=(0.0, 0.0), angle=0.0), # front-front
            DistanceSensor(self, pos=(0.0, 0.0), angle=0.0), # front-left
            DistanceSensor(self, pos=(0.0, 0.0), angle=0.0), # front-right
            DistanceSensor(self, pos=(0.0, 0.0), angle=0.0), # left
            DistanceSensor(self, pos=(0.0, 0.0), angle=0.0)  # right
        ]

        self.digital_sensors = [
            DigitalSensor(self, pos=(0.0, 0.0)), # front-left
            DigitalSensor(self, pos=(0.0, 0.0)), # front-right
            DigitalSensor(self, pos=(0.0, 0.0))  # back
        ]

        self.arena.add_robot(self)

    def set_motor_commands(self, rot_vel_wheel_left, rot_vel_wheel_right):
        self.rot_vel_wheel_left = rot_vel_wheel_left
        self.rot_vel_wheel_right = rot_vel_wheel_right

    def step(self, dt):
        # Model inspiration from
        # http://kdm.p.lodz.pl/articles/2011/15_4_5.pdf

        vl = self.rot_vel_wheel_left  * self.wheel_radius
        vr = self.rot_vel_wheel_right * self.wheel_radius

        beta_dot = (vr - vl)/self.size

        self.angle += beta_dot * dt

        avg_vel = (vl + vr)/2.0

        x_dot = avg_vel * math.cos(self.angle)
        y_dot = avg_vel * math.sin(self.angle)

        self.pos += np.matrix([[x_dot], [y_dot]]) * dt

    def sensor_values(self):
        vals = [sensor.value() for sensor in self.distance_sensors] + \
            [np.float32(sensor.value()) for sensor in self.digital_sensors]
        return np.array(vals)

    def corners(self):
        p0 = np.matrix([[self.size], [self.size]]) / 2.0
        angles = [self.angle + n*math.pi/2.0 for n in range(4)]
        return [self.pos + rotate(p0, angle) for angle in angles]

    def is_inside(self, pos):
        W = H = self.size/2.0
        delta = pos-self.pos
        delta_rel_coord = rotate(delta, -self.angle)
        return (abs(delta_rel_coord[0]) <= W) and (abs(delta_rel_coord[1]) <= H)

    def has_collided(self):
        my_corners = self.corners()
        for enemy in self.arena.get_enemies(of_robot=self):
            for corner in enemy.corners():
                if self.is_inside(corner):
                    return True

            for corner in my_corners:
                if enemy.is_inside(corner):
                    return True

        return False

    def is_outside(self):
        return np.linalg.norm(self.pos) > self.arena.radius

    def state(self):
        return np.array([self.pos.item(0), self.pos.item(1), self.angle])