import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class SumoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Two control signals: left and right motor command, each within -1 to 1
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)

        self.reset()

    def step(self, action):
        self.nof_steps += 1

        self.state = self.observation_space.sample() + 1

        reward = np.float32(1.0)

        is_done = (self.nof_steps == 10)

        return self.state, reward, is_done, {}

    def reset(self):
        self.state = self.observation_space.sample()
        self.nof_steps = 0

        return self.state

    def render(self, mode='human'):
        print("sumo.render()")

    def close(self):
        print("sumo.close()")
