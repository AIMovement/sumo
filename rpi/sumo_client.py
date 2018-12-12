from time import sleep

import grpc
import sumo_pb2
import sumo_pb2_grpc

def generate_commands():
    messages = [
        sumo_pb2.MotorCommand(left=0.1, right=0.2),
    ]
    for msg in messages:
        print("Sending command {0}".format(msg))
        yield msg

def communicate(stub):
    sleep(1.0)
    responses = stub.SumoIO(generate_commands())
    for response in responses:
        print("Received sensors {0}".format(response))

if __name__ == '__main__':
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sumo_pb2_grpc.SumoProtocolStub(channel)
        communicate(stub)
