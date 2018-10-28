import pyglet
import gym_sumo.envs.resources

import math

import threading

from pyglet.window import key

class Robot(pyglet.sprite.Sprite):

    def __init__(self, robot, *args, **kwargs):
        super(Robot, self).__init__(img=gym_sumo.envs.resources.sumo_image, *args, **kwargs)

        self.bot = robot

        #self.keys = dict(left=False, right=False)

        self.update()

    # def on_key_press(self, symbol, modifiers):
    #     if symbol == key.LEFT:
    #         self.keys['left'] = True
    #     elif symbol == key.RIGHT:
    #         self.keys['right'] = True

    # def on_key_release(self, symbol, modifiers):
    #     if symbol == key.LEFT:
    #         self.keys['left'] = False
    #     elif symbol == key.RIGHT:
    #         self.keys['right'] = False

    def update(self):
        state = self.bot.state()

        print(state)

        M_TO_MM = 1000.0
        self.x = M_TO_MM * state[0]
        self.y = M_TO_MM * state[1]

        #self.y = -self.y

        self.rotation = math.degrees(state[2])

class Dohyo(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(Dohyo, self).__init__(img=gym_sumo.envs.resources.dohyo_image, *args, **kwargs)

class Visualizer(pyglet.window.Window):

    def __init__(self, arena, *args, **kwargs):
        super(Visualizer, self).__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()

        self.arena = arena

        self.dohyo = Dohyo(x=self.width/2, y=self.height/2, batch=self.batch)

        self.robots = [Robot(r, batch=self.batch) for r in arena.bots]

        for robot in self.robots:
            self.push_handlers(robot)

        #pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        for obj in self.robots:
            obj.update()
            obj.x += self.width/2
            obj.y += self.height/2

        self.switch_to()
        self.dispatch_events()
        self.flip()
        self.on_draw()

    def update2(self):
        self.on_draw

class RenderThread(threading.Thread):
    def __init__(self, arena):
        threading.Thread.__init__(self)
        self.arena = arena
        self.win = None

    def run(self):
        print("Starting render thread...")
        self.win = Visualizer(self.arena, width=800, height=800)
        pyglet.clock.schedule_interval(self.win.update, 1 / 60.0)
        pyglet.app.run()

    def stop(self):
        self.win.close()

    def update(self):
        if not self.win is None:
            self.win.update()