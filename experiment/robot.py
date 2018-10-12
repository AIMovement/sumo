import math
import pyglet
from pyglet.window import key
import resources


class Robot(pyglet.sprite.Sprite):
    """Physical object that responds to user input"""

    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(img=resources.sumo_image, *args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.beta = 0.0

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
        # Model inspiration from
        # http://kdm.p.lodz.pl/articles/2011/15_4_5.pdf

        ROBOT_WIDTH = 0.10
        WHEEL_RADIUS = 0.015
        M_TO_MM = 1000.0

        vr = 2.0*math.pi*WHEEL_RADIUS if self.keys['right'] else 0.0
        vl = 2.0*math.pi*WHEEL_RADIUS if self.keys['left'] else 0.0

        beta_dot = (vr - vl)/ROBOT_WIDTH

        self.beta = self.beta + beta_dot * dt

        avg_vel = (vl + vr)/2.0

        x_dot = avg_vel * math.cos(self.beta)
        y_dot = avg_vel * math.sin(self.beta)

        y_dot = -1.0 * y_dot    # y-axis in image is down => invert

        self.x = self.x + M_TO_MM * x_dot * dt
        self.y = self.y + M_TO_MM * y_dot * dt

        self.rotation = math.degrees(self.beta)

        self.check_bounds()