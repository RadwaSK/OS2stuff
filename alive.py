import zmq
import sys
import time


def sendAliveMsg(node_id, port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:%s" % port)

    while True:
        msg = {'Alive': 'yes', 'node_id': node_id}
        socket.send_pyobj(msg)
        time.sleep(1)


p = sys.argv[1]
ID = sys.argv[2]
sendAliveMsg(ID, p)
