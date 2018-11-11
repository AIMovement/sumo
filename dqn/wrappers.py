import gym
import gym.spaces
import numpy as np

class DiscretizeActionWrapper(gym.ActionWrapper):

    def __init__(self, env, speed = 15.0):
        '''
            Overrides the continuous action space with a discrete version.
            Actions:
                Num     Action (Motor left, Motor right)
                0       (-1, -1)
                1       (-1,  0)
                2       (-1,  1)
                3       ( 0, -1)
                4       ( 0,  0)
                5       ( 0,  1)
                6       ( 1, -1)
                7       ( 1,  0)
                8       ( 1,  1)
        '''
        super(DiscretizeActionWrapper, self).__init__(env)
        self.action_space = gym.spaces.Discrete(9)
        self._speed = speed

    def action(self, action):
        if action in [0,1,2]:
            left = -self._speed
        elif action in [3,4,5]:
            left = 0.0
        elif action in [6,7,8]:
            left = self._speed

        if action in [0,3,6]:
            right = -self._speed
        elif action in [1,4,7]:
            right = 0.0
        elif action in [2,5,8]:
            right = self._speed

        return (left, right)


class BufferWrapper(gym.ObservationWrapper):
    def __init__(self, env, n_steps, dtype=np.float32):
        super(BufferWrapper, self).__init__(env)
        self.dtype = dtype
        old_space = env.observation_space
        self.old_shape = env.observation_space.shape
        self.observation_space = gym.spaces.Box(old_space.low.repeat(n_steps, axis=0),
                                                old_space.high.repeat(n_steps, axis=0), dtype=dtype)

    def reset(self):
        self.buffer = np.zeros_like(self.observation_space.low, dtype=self.dtype)
        return self.observation(self.env.reset())

    def observation(self, observation):
        n = self.old_shape[0]
        self.buffer[:-n] = self.buffer[n:]
        self.buffer[-n:] = observation
        return self.buffer

def make_env(env_name):
    env = gym.make(env_name)
    env = DiscretizeActionWrapper(env)
    return BufferWrapper(env, 4)
