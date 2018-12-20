from time import sleep

import grpc
import sumo_pb2
import sumo_pb2_grpc

import pyglet
from pyglet.window import key
from collections import deque
import threading
import argparse

WIN_WIDTH = 640
WIN_HEIGHT = 480

class KeyboardListener(object):

    def __init__(self, win, cmdqueue):
        super(KeyboardListener, self).__init__()

        self.cmdqueue = cmdqueue

        self.keyboard = pyglet.window.key.KeyStateHandler()

        win.push_handlers(self.keyboard)

        self._cmd = (0.0, 0.0)
        self.cmdqueue.append(self._cmd)

        pyglet.clock.schedule_interval(self.command_update, 0.05)

    def is_pressed(self, k):
        return self.keyboard[k]

    def command_update(self, dt):
        if self.is_pressed(key.Q):
            quit()

        elif self.is_pressed(key.UP):
            if self.is_pressed(key.LEFT):
                cmd = (0.5, 1.0)
            elif self.is_pressed(key.RIGHT):
                cmd = (1.0, 0.5)
            elif self.is_pressed(key.DOWN):
                cmd = (0.0, 0.0)
            else:
                cmd = (1.0, 1.0)

        elif self.is_pressed(key.LEFT):
            if self.is_pressed(key.DOWN):
                cmd = (-0.5, -1.0)
            elif self.is_pressed(key.RIGHT):
                cmd = (0.0, 0.0)
            else:
                cmd = (-0.5, 0.5)

        elif self.is_pressed(key.RIGHT):
            if self.is_pressed(key.DOWN):
                cmd = (-1.0, -0.5)
            else:
                cmd = (0.5, -0.5)

        elif self.is_pressed(key.DOWN):
            cmd = (-1.0, -1.0)

        else:
            cmd = (0.0, 0.0)

        scale = 0.5
        cmd = (scale*cmd[0], scale*cmd[1])

        if cmd != self._cmd:
            self.cmdqueue.append(cmd)
            self._cmd = cmd

class Visualizer(pyglet.window.Window):

    def __init__(self, sensorqueue, *args, **kwargs):
        super(Visualizer, self).__init__(*args, **kwargs)

        self.sensorqueue = sensorqueue

        self.batch = pyglet.graphics.Batch()

        names = '\n'.join(['front',
                           'front-left',
                           'front-right',
                           'left',
                           'right',
                           'ground-left',
                           'ground-right',
                           'ground-back'])

        self.value_template = '\n'.join(['{'+str(i)+'}' for i in range(8)])

        self.sensor_value_names = pyglet.text.Label(names,
                                font_name=('Verdana', 'Helvetica', 'Arial'),
                                font_size=9,
                                x=10,
                                y=WIN_HEIGHT-10,
                                multiline=True,
                                width=WIN_WIDTH/4,
                                anchor_x='left',
                                anchor_y='top',
                                batch=self.batch)

        self.sensordata = pyglet.text.Label('',
                                font_name=('Verdana', 'Helvetica', 'Arial'),
                                font_size=9,
                                x=150,
                                y=WIN_HEIGHT-10,
                                multiline=True,
                                width=WIN_WIDTH/4,
                                anchor_x='left',
                                anchor_y='top',
                                batch=self.batch)

        self.description = pyglet.text.Label('Use arrow keys to move robot. Press Q to quit.',
                                font_name=('Verdana', 'Helvetica', 'Arial'),
                                font_size=12,
                                x=10,
                                y=10,
                                anchor_x='left',
                                anchor_y='bottom',
                                batch=self.batch)

        self.push_handlers(self.sensordata)
        self.push_handlers(self.sensor_value_names)
        self.push_handlers(self.description)

        pyglet.clock.schedule_interval(self.update, 1 / 10.0)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        last_values = None
        while len(self.sensorqueue) > 0:
            last_values = self.sensorqueue.popleft()

        if last_values is not None:
            #print(last_values)
            self.sensordata.text = self.value_template.format(last_values.distance.front_front,
                                                              last_values.distance.front_left,
                                                              last_values.distance.front_right,
                                                              last_values.distance.left,
                                                              last_values.distance.right,
                                                              last_values.ground.left,
                                                              last_values.ground.right,
                                                              last_values.ground.back)

def generate_commands(cmdqueue):
    while True:
        sleep(0.01)
        while len(cmdqueue) > 0:
            cmd = cmdqueue.popleft()
            #print("Sending command {0}".format(cmd))
            yield sumo_pb2.MotorCommand(left=cmd[0], right=cmd[1])

def communicate(stub, cmdqueue, sensorqueue):
    sleep(1.0)
    responses = stub.SumoIO(generate_commands(cmdqueue))
    for response in responses:
        #print("Received sensors {0}".format(response))
        sensorqueue.append(response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='localhost:50051', help='IP-address for server')
    args = parser.parse_args()

    cmdqueue = deque()
    sensorqueue = deque()

    win = Visualizer(sensorqueue, width=WIN_WIDTH, height=WIN_HEIGHT)

    ctrl = KeyboardListener(win, cmdqueue)

    def handle_protocol():
        # NOTE(gRPC Python Team): .close() is possible on a channel and should be
        # used in circumstances in which the with statement does not fit the needs
        # of the code.
        with grpc.insecure_channel(args.address) as channel:
            stub = sumo_pb2_grpc.SumoProtocolStub(channel)
            communicate(stub, cmdqueue, sensorqueue)

    thread = threading.Thread(target=handle_protocol)
    thread.daemon = True
    thread.start()

    pyglet.app.run()
