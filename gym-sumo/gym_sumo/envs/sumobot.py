import numpy as np
from numpy import dot
from numpy.linalg import norm
import math

def rotate(vec, angle):
    c, s = math.cos(angle), math.sin(angle)
    return dot(np.array([[c,-s], [s, c]]), vec)

class DistanceSensor(object):
    def __init__(self, robot, arena, x0, y0, angle):
        self.robot = robot
        self.arena = arena
        self.offset = np.array([[x0], [y0]])
        self.angle = angle

        self.alfa = math.radians(9.8)
        self.beta = math.radians(1.6)

        self.raw_per_dist = (500.0-200.0)/(0.15-0.45)

    def normal(self):
        return rotate(self.offset, self.robot.get_angle())

    def position(self):
        return self.robot.position() + self.normal()

    def get_angle(self):
        return self.robot.get_angle() + self.angle

    def is_observable(self, pos, v):
        v_a, v_b = v
        p_ccw_of_b = (v_b[0]*pos[1] - v_b[1]*pos[0]) > 0 # cross_z
        a_ccw_of_p = (pos[0]*v_a[1] - pos[1]*v_a[0]) > 0 # cross_z
        return a_ccw_of_p and p_ccw_of_b

    def distance_to_raw_value(self, dist):
        # Might need to improve this, see notebook...
        return min(max(500.0 + self.raw_per_dist * (dist-0.15), 0.0), 550)

    def value(self):
        pos = self.position()
        n = self.normal()
        v = (rotate(n, self.alfa), rotate(n, -self.beta))
        closest = np.finfo(np.float32).max
        for enemy in self.arena.get_enemies(of_robot=self.robot):
            corners = enemy.corners()
            for i, _ in enumerate(corners):
                c0, c1 = corners[i], corners[(i+1) % len(corners)]
                for a in np.arange(0.0, 1.0, 0.2):
                    c_test = a * c0 + (1.0-a) * c1
                    p = c_test - pos
                    if self.is_observable(p, v):
                        closest = min(closest, norm(p))

        return self.distance_to_raw_value(closest)

class DigitalSensor(object):
    def __init__(self, robot, arena, x0, y0):
        self.robot = robot
        self.arena = arena
        self.offset = np.array([[x0], [y0]])

    def normal(self):
        return rotate(self.offset, self.robot.get_angle())

    def position(self):
        return self.robot.position() + self.normal()

    def value(self):
        r_outer = self.arena.radius
        r_inner = r_outer-self.arena.edge_width
        return r_inner <= norm(self.position()) <= r_outer

class Sumobot(object):

    def __init__(self, arena, x0, y0, angle0=0.0):
        self.arena = arena
        self.pos = np.array([[x0], [y0]])
        self.angle = angle0

        self.rot_vel_wheel_right = 0.0
        self.rot_vel_wheel_left = 0.0

        self.size = 0.10
        self.wheel_radius = 0.015

        self.distance_sensors = [
            DistanceSensor(self, arena, x0=0.04,  y0=0.0,   angle=0.0),          # front-front
            DistanceSensor(self, arena, x0=0.035, y0=0.02,  angle=math.pi/2/4),  # front-left
            DistanceSensor(self, arena, x0=0.035, y0=-0.02, angle=-math.pi/2/4), # front-right
            DistanceSensor(self, arena, x0=0.0,   y0=0.03,  angle=math.pi/2),    # left
            DistanceSensor(self, arena, x0=0.0,   y0=-0.03, angle=-math.pi/2)    # right
        ]

        self.digital_sensors = [
            DigitalSensor(self, arena, x0=0.03, y0=0.04),  # front-left
            DigitalSensor(self, arena, x0=0.03, y0=-0.04), # front-right
            DigitalSensor(self, arena, x0=-0.045, y0=0.0)  # back
        ]

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

        self.pos += np.array([[x_dot], [y_dot]]) * dt

    def sensor_values(self):
        vals = [sensor.value() for sensor in self.distance_sensors] + \
            [np.float32(sensor.value()) for sensor in self.digital_sensors]
        return np.array(vals)

    def corners(self):
        p0 = np.array([[self.size], [self.size]]) / 2.0
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
        return norm(self.pos) > self.arena.radius

    def position(self):
        return self.pos

    def get_angle(self):
        return self.angle

    def state(self):
        return np.array([self.pos[0], self.pos[1], self.angle])