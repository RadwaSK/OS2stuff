import zmq
import sys
import os
import time

def upload(socket, order):
    print("sending upload req. to master")
    socket.send_pyobj({'req': order[0], 'filename': order[1]})
    #  Get the reply.
    message = socket.recv_pyobj()
    print("received reply from master")
    # If I can upload
    if message["op"] == "success":
        path = 'clientVideos/' + order[1]
        video = open(path, 'rb').read()
        dk_socket = context.socket(zmq.PAIR)
        dk_socket.connect(message["address"])  # ip:port
        print("connected to datakeeper & ready to upload")
        dk_socket.send_pyobj({"req": "upload", "filename": order[1], "video": video, 'checkWithMaster': True})
        print("file is sent to datakeeper successfully")
        dk_socket.close()
    else:
        print("file is already uploaded")
    


def download(socket, order):
    # Send req Download and file name to master
    req_msg = {'req': order[0], 'filename': order[1], 'checkWithMaster': True}
    socket.send_pyobj(req_msg)
    print("request sent to master")
    #  Get the reply from master if the file exists or not
    message = socket.recv_pyobj()
    print("reply received from master")
    # If I can upload
    if message['op'] == "found":
        print("file is found")
        # Open a client socket to connect to the data keeper
        dk_socket = context.socket(zmq.PAIR)
        print("Connecting to datakeeper...")
        dk_socket.connect(message["address"])  # tcp://ip:port
        print("Connected to Datakeeper successfully")
        dk_socket.send_pyobj(req_msg)
        print("request sent to datakeeper")
        # receiving the file from the data keeper
        msg = dk_socket.recv_pyobj()
        print("File is received from datakeeper. closing socket...")
        dk_socket.close()
        filename = msg['filename']
        if not os.path.exists("downloadedVideos"):
            os.mkdir("downloadedVideos")
        path = 'downloadedVideos/' + filename
        video = msg['video']
        with open(path, "wb") as output:
            output.write(video)
    else:
        print("file is not found in any data keeper")


#run as python3 client.py 192.168.1.2 3


os.system("hostname -I >> ip.txt")
os.system("hostname -I >> ip.txt")

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

ip = data[0].split()[0]

Nport = sys.argv[1] # Number of processes of master / number of servers example: 3

context = zmq.Context()
# socket of client, type client, connect to all listenToClient servers in master
socket = context.socket(zmq.REQ)
for i in range(int(Nport)):
    socket.connect ("tcp://"+ip+":"+str(i+5555))

while True:
    order = input("enter your order: ")
    # upload video.mp4
    order = order.split()
    if order[0] == "upload":
        upload(socket, order)
    elif order[0] == "download":
        download(socket, order)
    else:
        print("undefined")
