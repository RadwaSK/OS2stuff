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
    # Receive from client or master in N-replicate process
    msg = socket.recv_pyobj()

    if msg["req"] == "upload":
        filename = msg['filename']
        if not os.path.exists('videos'):
            os.mkdir('videos')

        path = 'videos/' + filename
        video = msg['video']
        with open (path,"wb") as output:
            output.write(video)

        """ This is to be un-commented if datakeeper should reply with a success msg on who ever
            is requesting the upload. And since it's server, I think it should """
        # socket.send_pyobj({'success': True})

    elif msg["req"] == "download":
        filename = msg['filename']
        video = open(order[1],'rb').read()
        msg_to_client = {'filename': filename, 'video': video}
        socket.send_pyobj(msg_to_client)


    
