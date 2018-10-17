import numpy as np

class Arena(object):

    def __init__(self):
        self.bots = list()

    def add_robot(self, robot):
        self.bots.append(robot)

    def update(self, dt):
        for r in self.bots:
            r.step(dt)