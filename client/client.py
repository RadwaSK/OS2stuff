import zmq
import sys
import time


def upload(socket, order):
    socket.send_pyobj(order)
    #  Get the reply.
    message = socket.recv_pyobj()
    # If I can upload
    if message["op"] == "success":
        video = open(order[1],'rb').read()
        dk_socket = context.socket(zmq.REQ)
        dk_socket.connect(message["address"]) #ip:port
        dk_socket.send_pyobj({"req":"upload","filename":order[1],"video":video})
        dk_socket.close()
    else:
        print("file is already uploaded")
    


def download(socket, order):
    socket.send ("Hello")
    #  Get the reply.
    message = socket.recv()

ip = sys.argv[1] # IP master
Nport = sys.argv[2] # Number of processes of master / number of servers

context = zmq.Context()
# socket of client, type client, connect to all listenToClient servers in master
socket = context.socket(zmq.REQ)
for i in range(int(Nport)):
    socket.connect ("tcp://%s:%s" % ip % str(i+5555))

while True:
    order = input("enter your order :")
    # upload video.mp4
    order = order.split()
    if order[0] == "upload":
        upload(socket, order)
    elif order[0] == "download":
        download(socket, order)
    else:
        print("undefined")
