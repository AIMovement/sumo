import numpy as np

class Arena(object):

    def __init__(self):
        self.bots = list()
        self.radius = 0.77 / 2.0
        self.edge_width = 0.025

    def add_robot(self, robot):
        self.bots.append(robot)

    def remove_robot(self, robot):
        self.bots.remove(robot)

    def update(self, dt):
        for r in self.bots:
            r.step(dt)

    def get_enemies(self, of_robot):
        return [robot for robot in self.bots if robot != of_robot]