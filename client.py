import zmq
import sys
import time


def upload(socket, order):
    socket.send_pyobj (order)
    #  Get the reply.
    message = socket.recv_pyobj()
    if message["op"]=="success":
        video=open(order[1],'rb').read()
        socket.close()
        socket.connect(message["address"])
        socket.send_pyobj({order[1]:video})
    else:
        print("file is already uploaded")
    


def download(socket, order):
    socket.send ("Hello")
    #  Get the reply.
    message = socket.recv()

ip = sys.argv[1]
Nport = sys.argv[2]

context = zmq.Context()
socket = context.socket(zmq.REQ)
for i in range(int(Nport)):
    socket.connect ("tcp://%s:%s" % ip % str(i+5555))

while True:
    order = input("enter your order :")
    order = order.split()
    if order[0] == "upload":
        upload(socket, order)
    elif order[0] == "download":
        download(socket, order)
    else:
        print("undefined")
