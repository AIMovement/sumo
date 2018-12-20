#!/usr/bin/python3

from robot_communication import Robot_IO
import time

import grpc
import sumo_pb2
import sumo_pb2_grpc

from collections import deque
from concurrent import futures
import threading
import argparse

class Remote_IO(sumo_pb2_grpc.SumoProtocolServicer):
    ''' Receive commands and send sensor data via grpc.
    Store commands in and get sensor data from thread safe queues'''
    def __init__(self, cmdqueue, sensorqueue):
        super(Remote_IO, self).__init__()

        self.cmdqueue = cmdqueue
        self.sensorqueue = sensorqueue

    def convert_sensor(self, sensordata):
        return sumo_pb2.Sensors(
                    distance=sumo_pb2.DistanceSensors(
                                front_left=sensordata.front_left,
                                front_front=sensordata.front,
                                front_right=sensordata.front_right,
                                left=sensordata.left,
                                right=sensordata.right),
                    ground=sumo_pb2.GroundSensors(
                                left=sensordata.bottom_left,
                                right=sensordata.bottom_right,
                                back=sensordata.bottom_back))

    def convert_command(self, cmd):
        return (cmd.left, cmd.right)

    def SumoIO(self, request_iterator, context):

        def incoming_commands():
            while True:
                time.sleep(0.01)
                for cmd in request_iterator:
                    print(cmd)
                    self.cmdqueue.append(self.convert_command(cmd))

        thread = threading.Thread(target=incoming_commands)
        thread.daemon = True
        thread.start()

        def sensor_values():
            while True:
                time.sleep(0.01)
                while len(self.sensorqueue) > 0:
                    yield self.sensorqueue.popleft()

        output = sensor_values()

        while True:
            yield self.convert_sensor(next(output))

def SerialTasks(rio, cmdqueue, sensorqueue):
    while True:
        while len(cmdqueue) > 0:
            cmd = cmdqueue.popleft()
            rio.send_motor_commands(left=cmd[0], right=cmd[1])

        s = rio.get_sensors()
        if s is not None:
            sensorqueue.append(s)

        time.sleep(0.02)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--ip_port', default='50051', help='IP-port used for remote mode')
    parser.add_argument('-s', '--serial_port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('-b', '--baud', default='115200', help='Baudrate')
    args = parser.parse_args()

    cmdqueue = deque()
    sensorqueue = deque()

    #rio = Robot_IO('/dev/tty.usbserial-DJ004U9C', '115200')#/dev/ttyUSB0', '115200')
    rio = Robot_IO(args.serial_port, args.baud)
    rio.connect()

    while not rio.is_pending_data():
        time.sleep(0.10)

    executor = futures.ThreadPoolExecutor(max_workers=10)
    robot_serial = executor.submit(SerialTasks, rio, cmdqueue, sensorqueue)

    remote = Remote_IO(cmdqueue, sensorqueue)
    server = grpc.server(executor)
    sumo_pb2_grpc.add_SumoProtocolServicer_to_server(remote, server)
    server.add_insecure_port('[::]:{0}'.format(args.ip_port))
    server.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        rio.disconnect()
        server.stop(0)


