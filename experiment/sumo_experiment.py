import pyglet, random, math
import robot, resources

class Vec2(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def dot(self, v):
        return self.x * v.x + self.y * y

    def __add__(self, v):
        return Vec2(self.x+v.x, self.y+v.y)

    def __sub__(self, v):
        return Vec2(self.x-v.x, self.y-v.y)

    def rotate(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Vec2(c*self.x - s*self.y, s*self.x + c*self.y)

    def __str__(self):
        return "({},{})".format(self.x, self.y)

def center(r):
    return Vec2(r.x, r.y)

def corners(r):
    W = r.width/2 * 0.9
    H = r.height/2 * 0.9
    c0 = Vec2(W, H).rotate(-math.radians(r.rotation))
    return [center(r) + c0, center(r) + c0.rotate(math.pi/2.0), center(r) + c0.rotate(math.pi), center(r) + c0.rotate(3.0*math.pi/2.0)]

def is_inside(r, v):
    W = r.width/2 * 0.9
    H = r.height/2 * 0.9
    p0 = center(r)
    p = v - p0
    w = p.rotate(math.radians(r.rotation))
    return (-W < w.x < W) and (-H < w.y < H)

def is_colliding(ra, rb):
    for c in corners(rb):
        if is_inside(ra, c):
            return True

    return False

class Visualizer(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Visualizer, self).__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()
        self.robots = list()

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)


        self.c = 0

    def on_draw(self):
        self.clear()
        self.batch.draw()



    def update(self, dt):
        for a in self.robots:
            for b in self.robots:
                if a != b and is_colliding(a, b):
                    print(str(self.c) + " ouch! " + str((a,b)))
                    self.c += 1

        for obj in self.robots:
            #print(center(obj))
            #print("c = " + ";".join(map(str,corners(obj))))
            obj.update(dt)
            print(obj.rotation)

    def add_robot(self, robot):
        self.robots.append(robot)
        self.push_handlers(robot)

if __name__ == "__main__":

    vis = Visualizer(width=800, height=600)

    r_fixed = robot.Robot(controllable=False, x=550, y=400, batch=vis.batch)
    r_fixed.rotation = 30

    vis.add_robot(r_fixed)
    vis.add_robot(robot.Robot(controllable=True, batch=vis.batch))

    pyglet.app.run()
