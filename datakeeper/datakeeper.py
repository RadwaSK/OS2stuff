import zmq
import sys
import os

port = sys.argv[1] # port of the datakeeper

context = zmq.Context()
# Socket, type server
socket = context.socket(zmq.REQ)

os.system("hostname -I >> ip.txt")

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

socket.bind("tcp://%s:%s" %data[0] %port)

while True :
    # master msg
    # Receive from client
    msg = socket.recv_pyobj()

    if msg["req"]=="upload":
        filename = msg['filename']
        if not os.path.exists('videos'):
            os.mkdir('videos')

        path = 'videos/' + filename
        video = msg['video']
        with open (path,"wb") as output:
            output.write(video)

    elif msg["req"] == "download":
        filename = msg['filename']
        video = open(order[1],'rb').read()
        msg_to_client = {'filename': filename, 'video': video}
        socket.send_pyobj(msg_to_client)
        pass

    
