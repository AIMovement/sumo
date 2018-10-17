import sumobot
import math
import pyglet
from pyglet.window import key
import resources


class Robot(pyglet.sprite.Sprite):
    """Physical object that responds to user input"""

    def __init__(self, controllable, *args, **kwargs):
        super(Robot, self).__init__(img=resources.sumo_image, *args, **kwargs)

        self.controllable = controllable

        self.bot = sumobot.Sumobot(x0=0.0, y0=0.0)

        self.keys = dict(left=False, right=False)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.keys['left'] = True
        elif symbol == key.RIGHT:
            self.keys['right'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.keys['left'] = False
        elif symbol == key.RIGHT:
            self.keys['right'] = False

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def update(self, dt):
        if not self.controllable:
            return

        vr = 2.0*math.pi if self.keys['right'] else 0.0
        vl = 2.0*math.pi if self.keys['left'] else 0.0

        self.bot.step(dt, rot_vel_wheel_left=vl, rot_vel_wheel_right=vr)

        s = self.bot.state()

        self.rotation = math.degrees(s[2])

        M_TO_MM = 1000.0
        self.x = M_TO_MM * self.bot.pos[0]
        self.y = M_TO_MM * self.bot.pos[1]

        self.y = -self.y

        self.check_bounds()
