# Install sumo-gym before running:
# > cd gym-sumo && pip install -e .

import gym
import gym_sumo

import numpy as np

import time

if __name__ == "__main__":
    env = gym.make("sumo-v0")

    env.reset()

    r = 0.0
    is_done = False

    for _ in np.arange(0.0, 5.0, env.time_step):
        env.render()
        time.sleep(env.time_step)
        action = env.action_space.sample()
        obs, reward, is_done, _ = env.step((15,5))
        #print(obs)
        r += reward
        if is_done:
            break

    env.close()

    print("Total reward {0}".format(r))