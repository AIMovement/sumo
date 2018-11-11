#!/usr/bin/env python3

'''
    Install sumo-gym before running:
    > cd gym-sumo && pip install -e .
'''

import gym
import gym_sumo

import numpy as np

def main(env):

    env.reset()

    r = 0.0
    is_done = False

    for _ in np.arange(0.0, 5.0, 0.02):
        env.render()
        action = (15,5) # env.action_space.sample()
        obs, reward, is_done, _ = env.step(action)
        #print(obs)
        r += reward
        if is_done:
            break

    env.close()

    print("Total reward {0}".format(r))

if __name__ == "__main__":
    env = gym.make("sumo-v0")

    #import cProfile
    #cProfile.run('main(env)', sort=1)
    main(env)