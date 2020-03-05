import zmq
import sys
import time


def upload(socket, order):
    socket.send ("Hello")
    #  Get the reply.
    message = socket.recv()


def download(socket, order):
    socket.send ("Hello")
    #  Get the reply.
    message = socket.recv()


ip = sys.argv[1]
port = sys.argv[2]

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://%s:%s" % ip % port)

while True:
    order = input("enter your order :")
    order = order.split()
    if order[0] == "upload":
        upload(socket, order)
    elif order[0] == "download":
        download(socket, order)
    else:
        print("undefined")
