from gym_sumo.envs.arena import Arena
from gym_sumo.envs.sumobot import Sumobot
from gym.envs.classic_control import rendering

import numpy as np
from numpy.linalg import norm
import math

import pyglet

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class SumoEnv(gym.Env):
    """
    Actions:
        Num Action                              Min     Max
        0   Control signal for left motor       -1.0    1.0
        1   Control signal for right motor      -1.0    1.0

    Observation:
        Num Observation                         Min     Max
        0   Robot front sensor value            0.0     +Inf
        1   Robot front-left sensor value       0.0     +Inf
        2   Robot front-right sensor value      0.0     +Inf
        3   Robot left sensor value             0.0     +Inf
        4   Robot right sensor value            0.0     +Inf
        5   Robot digital front-left value      0.0     1.0
        6   Robot digital front-right value     0.0     1.0
        7   Robot digital back value            0.0     1.0

    """

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    TIME_STEP = 0.02

    def __init__(self):
        # Two control signals: left and right motor command, each within -1 to 1
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        low = np.zeros(8)
        high = np.array([
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            1.0,
            1.0,
            1.0])

        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.viewer = None

        self.reset()

    def step(self, action):
        self.nof_steps += 1

        enemy_action = (0,0) #self.action_space.sample()

        self.robot.set_motor_commands( \
            rot_vel_wheel_left=action[0], \
            rot_vel_wheel_right=action[1])

        self.enemy.set_motor_commands( \
            rot_vel_wheel_left=enemy_action[0], \
            rot_vel_wheel_right=enemy_action[1])

        self.arena.update(self.TIME_STEP)


        is_outside = self.robot.is_outside()
        has_collided = self.robot.has_collided()

        obs = self.robot.sensor_values()

        dist = norm(self.robot.position()-self.enemy.position())

        prev_dist = dist if self.prev_dist == None else self.prev_dist

        if is_outside:
            reward = -10000.0
        #elif self.enemy.is_outside():
        #    reward = 10.0
        elif has_collided:
            reward = 10000.0 - self.nof_steps
        else:
            reward = 1.0 if dist < prev_dist else -1.0

        self.prev_dist = dist

        is_done = is_outside or has_collided or self.nof_steps >= 3000

        return obs, reward, is_done, {}

    def reset(self):
        self.arena = Arena()

        if np.random.uniform() > 0.5:
            # Start positions set as per competition rules
            if np.random.uniform() > 0.5:
                y0 = 0.15
                enemy_th0 = math.pi
            else:
                y0 = -0.15
                enemy_th0 = math.pi/2

            self.robot = Sumobot(arena=self.arena, x0=0.15, y0=y0, angle0=0.0)
            self.arena.add_robot(self.robot)

            while True:
                p = np.random.uniform([0.1, 0.1], [0.8, 0.9], 2)
                r, th = self.arena.radius*p[0], math.pi*p[1]/2 + enemy_th0
                self.enemy = Sumobot(arena=self.arena, x0=r*math.cos(th), y0=r*math.sin(th), angle0=math.pi)
                self.arena.add_robot(self.enemy)
                if not self.enemy.is_outside() and not self.enemy.has_collided():
                    break
                self.arena.remove_robot(self.enemy)

        else:
            # Both starts totally at random
            while True:
                p = np.random.uniform([0.0, 0.0, 0.0], [0.8, 1.0, 1.0], 3)
                r, th, a0 = self.arena.radius*p[0], 2.0*math.pi*p[1], 2.0*math.pi*p[2]
                self.robot = Sumobot(arena=self.arena, x0=r*math.cos(th), y0=r*math.sin(th), angle0=a0)
                self.arena.add_robot(self.robot)
                if not self.robot.is_outside():
                    break
                self.arena.remove_robot(self.robot)

            while True:
                p = np.random.uniform([0.0, 0.0, 0.0], [0.8, 1.0, 1.0], 3)
                r, th, a0 = self.arena.radius*p[0], 2.0*math.pi*p[1], 2.0*math.pi*p[2]
                self.enemy = Sumobot(arena=self.arena, x0=r*math.cos(th), y0=r*math.sin(th), angle0=a0)
                self.arena.add_robot(self.enemy)
                dist = norm(self.robot.position()-self.enemy.position())
                if not self.enemy.is_outside() and not self.enemy.has_collided() and dist > 0.2:
                    break
                self.arena.remove_robot(self.enemy)

        #self.robot = Sumobot(arena=self.arena, x0=  0.15, y0=  0.15, angle0=0.0)
        #self.enemy = Sumobot(arena=self.arena, x0= -0.15, y0= -0.15, angle0=math.pi)

        self.nof_steps = 0
        self.prev_dist = None

        return self.robot.sensor_values()

    def render(self, mode='human'):
        M_TO_PIXEL = 1000.0
        screen_width = 800
        screen_height = 800
        show_sensor_pos = False

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            # Background color
            bg = rendering.FilledPolygon([(0,0), (0,screen_height), (screen_width,screen_height), (screen_width,0)])
            bg.set_color(0,0,0)
            self.viewer.add_geom(bg)

            # Dohyo
            self.dohyotrans = rendering.Transform()
            outer = rendering.make_circle(radius=M_TO_PIXEL*self.arena.radius, res=360)
            outer.set_color(1.0,1.0,1.0)
            outer.add_attr(self.dohyotrans)
            self.viewer.add_geom(outer)
            inner = rendering.make_circle(radius=M_TO_PIXEL*(self.arena.radius-self.arena.edge_width), res=360)
            inner.set_color(0,0,0)
            inner.add_attr(self.dohyotrans)
            self.viewer.add_geom(inner)
            L = 20
            cross_x = rendering.Line((-L,0), (L,0))
            cross_x.set_color(1.0,1.0,1.0)
            cross_x.add_attr(self.dohyotrans)
            self.viewer.add_geom(cross_x)
            cross_y = rendering.Line((0,-L), (0,L))
            cross_y.set_color(1.0,1.0,1.0)
            cross_y.add_attr(self.dohyotrans)
            self.viewer.add_geom(cross_y)
            self.dohyotrans.set_translation(screen_width/2, screen_height/2)

            # Robot and enemy
            W = M_TO_PIXEL*self.robot.size/2.0
            bot = rendering.FilledPolygon([(-W,-W), (W,-W), (W,W), (-W,W)])
            bot.set_color(0.6,0.6,0.6)
            arrow = rendering.FilledPolygon([(0,-W), (0,W), (W,0)])
            arrow.set_color(0.5,0.5,0.5)
            self.bottrans = rendering.Transform()
            bot.add_attr(self.bottrans)
            arrow.add_attr(self.bottrans)
            self.viewer.add_geom(bot)
            self.viewer.add_geom(arrow)

            if show_sensor_pos:
                self.senstran = list()
                for i, _ in enumerate(self.robot.distance_sensors):
                    sensor = rendering.FilledPolygon([(5,-12), (5,12), (-3,0)])
                    sensor.set_color(1,1,1)
                    t = rendering.Transform()
                    self.senstran.append(t)
                    sensor.add_attr(t)
                    self.viewer.add_geom(sensor)

            enmy = rendering.FilledPolygon([(-W,-W), (W,-W), (W,W), (-W,W)])
            enmy.set_color(0.6,0.6,0.6)
            arrow = rendering.FilledPolygon([(0,-W), (0,W), (W,0)])
            arrow.set_color(0.5,0.5,0.5)
            self.enmytrans = rendering.Transform()
            enmy.add_attr(self.enmytrans)
            arrow.add_attr(self.enmytrans)
            self.viewer.add_geom(enmy)
            self.viewer.add_geom(arrow)

        if show_sensor_pos:
            for i, s in enumerate(self.robot.distance_sensors):
                p = s.position()
                self.senstran[i].set_translation(screen_width/2+M_TO_PIXEL*p[0], screen_height/2+M_TO_PIXEL*p[1])
                self.senstran[i].set_rotation(s.get_angle())

        p = self.robot.position()
        self.bottrans.set_translation(screen_width/2+M_TO_PIXEL*p[0], screen_height/2+M_TO_PIXEL*p[1])
        self.bottrans.set_rotation(self.robot.get_angle())

        p = self.enemy.position()
        self.enmytrans.set_translation(screen_width/2+M_TO_PIXEL*p[0], screen_height/2+M_TO_PIXEL*p[1])
        self.enmytrans.set_rotation(self.enemy.get_angle())

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def __del__(self):
        self.close()
