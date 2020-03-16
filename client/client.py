import zmq
import sys
import os

def upload(socket, order):
    socket.send_pyobj({'req': order[0], 'filename': order[1]})
    #  Get the reply.
    message = socket.recv_pyobj()
    # If I can upload
    if message["op"] == "success":
        video = open(order[1],'rb').read()
        dk_socket = context.socket(zmq.PAIR)
        dk_socket.connect(message["address"]) #ip:port
        dk_socket.send_pyobj({"req": "upload", "filename": order[1], "video": video})
        print(message["address"])
        #dk_socket.close()
    else:
        print("file is already uploaded")
    


def download(socket, order):
    # Send req Download and file name to master
    req_msg = {'req': order[0], 'filename': order[1]}
    socket.send_pyobj(req_msg)
    #  Get the reply from master if the file exists or not
    message = socket.recv_pyobj()
    # If I can upload
    if message['op'] == "found":
        # Open a client socket to connect to the data keeper
        dk_socket = context.socket(zmq.REQ)
        dk_socket.connect(message["address"])  # tcp://ip:port
        # requesting the file from the data keeper having it
        dk_socket.send_pyobj(req_msg)
        # receiving the file from the data keeper
        msg = dk_socket.recv_pyobj()
        dk_socket.close()
        filename = msg['filename']
        path = 'videos/' + filename
        video = msg['video']
        with open(path, "wb") as output:
            output.write(video)
    else:
        print("file is not found in any data keeper")


#run as python3 client.py 192.168.1.2 3


ip = sys.argv[1] # IP master example : 192.168.1.2 
Nport = sys.argv[2] # Number of processes of master / number of servers example: 3

context = zmq.Context()
# socket of client, type client, connect to all listenToClient servers in master
socket = context.socket(zmq.REQ)
for i in range(int(Nport)):
    socket.connect ("tcp://"+ip+":"+str(i+5555))

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
