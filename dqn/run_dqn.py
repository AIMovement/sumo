#!/usr/bin/env python3
import gym
import gym_sumo

import time
import argparse
import numpy as np

import torch

import wrappers
import dqn_model
import gym.wrappers
import collections

ENV_NAME = "sumo-v0"
FPS = 50

VISUALIZE = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", required=True, help="Model file (.dat) to load")
    parser.add_argument("-r", "--record", help="Directory to store video recording")
    parser.add_argument("-n", "--number", default="1", help="Number of games")
    args = parser.parse_args()

    env = wrappers.make_env(ENV_NAME)
    if args.record:
        env = gym.wrappers.Monitor(env, args.record, video_callable=lambda episode_id: True)

    net = dqn_model.DuelingDQN(env.observation_space.shape, env.action_space.n)
    net.load_state_dict(torch.load(args.model, map_location=lambda storage, loc: storage))

    state = env.reset()
    total_reward = 0.0
    c = collections.Counter()

    nof_games = 0

    while nof_games < int(args.number):
        start_ts = time.time()
        if VISUALIZE:
            env.render()
        state_v = torch.tensor(np.array([state], copy=False))
        q_vals = net(state_v).data.numpy()[0]
        action = np.argmax(q_vals)
        c[action] += 1
        state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            nof_games += 1
            env.reset()

        if VISUALIZE:
            delta = 1/FPS - (time.time() - start_ts)
            if delta > 0:
                time.sleep(delta)
    print("Total reward: %.2f" % total_reward)
    print("Action counts:", c)

    env.close()
