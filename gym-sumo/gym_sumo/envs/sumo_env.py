from gym_sumo.envs.arena import Arena
from gym_sumo.envs.sumobot import Sumobot
from gym_sumo.envs.visualizer import Visualizer
from gym_sumo.envs.visualizer import RenderThread

import numpy as np
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

    metadata = {'render.modes': ['human']}

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

        self.time_step = 0.1

        self.vis = None

        self.reset()

    def step(self, action):
        self.nof_steps += 1

        enemy_action = self.action_space.sample()

        self.robot.set_motor_commands( \
            rot_vel_wheel_left=action[0], \
            rot_vel_wheel_right=action[1])

        self.enemy.set_motor_commands( \
            rot_vel_wheel_left=enemy_action[0], \
            rot_vel_wheel_right=enemy_action[1])

        self.arena.update(self.time_step)

        is_done = self.robot.has_collided() or self.robot.is_outside()

        # For now, just reward finding and running into enemy
        if self.robot.is_outside():
            reward = -1.0
        elif self.enemy.is_outside():
            reward = 2.0
        elif self.robot.has_collided():
            reward = 1.0
        else:
            reward = 0.0
        # we should also reward moving and finding enemy (low sensor values?)

        obs = self.robot.sensor_values()

        return obs, reward, is_done, {}

    def reset(self):
        self.arena = Arena()
        # Should place enemy (but not own robot?) at random within quadrant?
        self.robot = Sumobot(arena=self.arena, x0=  0.15, y0=  0.15, angle0=0.0)
        self.enemy = Sumobot(arena=self.arena, x0= -0.15, y0= -0.15, angle0=math.pi)

        self.nof_steps = 0

        if not self.vis is None:
            self.vis.close()

        self.vis = None

        return self.robot.sensor_values()

    def render(self, mode='human'):
        if self.vis is None:
            self.vis = Visualizer(self.arena, width=800, height=800)

        #pyglet.app.run()
        self.vis.update(1.0)

    def close(self):
        print("sumo.close()")
        #self.vis.stop()
