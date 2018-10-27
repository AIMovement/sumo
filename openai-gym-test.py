# Install sumo-gym before running:
# > cd gym-sumo && pip install -e .

import gym
import gym_sumo

if __name__ == "__main__":
    env = gym.make("sumo-v0")

    r = 0.0
    is_done = False

    while not is_done:
        action = env.action_space.sample()
        obs, reward, is_done, _ = env.step(action)
        print(obs)
        r += reward

    print("Total reward {0}".format(r))