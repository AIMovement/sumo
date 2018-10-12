import pyglet, random, math
import robot, resources

class Visualizer(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Visualizer, self).__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()
        self.robots = list()

        pyglet.clock.schedule_interval(self.update, 1 / 120.0)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        for obj in self.robots:
            obj.update(dt)

    def add_robot(self, robot):
        self.robots.append(robot)
        self.push_handlers(robot)

if __name__ == "__main__":

    vis = Visualizer(width=800, height=600)

    vis.add_robot(robot.Robot(x=400, y=300, batch=vis.batch))

    pyglet.app.run()
