import zmq
import sys
import os
import download




port= sys.argv[1]
context = zmq.Context()
socket = context.socket(zmq.REQ)
os.system("hostname -I >> ip.txt")
with open ("ip.txt", "r") as myfile:
    data=myfile.readlines()
socket.bind("tcp://%s:%s" %data[0] %port)

while True :
    #master msg
    msg=socket.recv_pyobj()
    if msg["req"]=="upload":
        filename = msg['filename']
        video = msg['video']
        with open (filename,"wb") as output:
            output.write(video)

    elif msg["req"] == "download":
        download.download(9999,socket)

    
