from concurrent import futures
from time import sleep

import grpc
import sumo_pb2
import sumo_pb2_grpc

class SumoProtocolServicer(sumo_pb2_grpc.SumoProtocolServicer):

    def __init__(self):
        super(SumoProtocolServicer, self).__init__()

    def SumoIO(self, request_iterator, context):
        for cmd in request_iterator:
            print("Command {0}".format(cmd))
            yield sumo_pb2.Sensors(
                    distance=sumo_pb2.DistanceSensors(
                                front_left=1,
                                front_front=2,
                                front_right=3,
                                left=4,
                                right=5
                            ),
                    ground=sumo_pb2.GroundSensors(
                                left=False,
                                right=True,
                                back=True
                            )
                )

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sumo_pb2_grpc.add_SumoProtocolServicer_to_server(
        SumoProtocolServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
