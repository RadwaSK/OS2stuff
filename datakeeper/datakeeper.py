import zmq
import sys
import os


#python3 datakeeper.py 6666

port = sys.argv[1] # port of the datakeeper

context = zmq.Context()
# Socket, type server
socket = context.socket(zmq.PULL)

os.system("hostname -I >> ip.txt")

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

socket.bind("tcp://*:"+port)

while True :
    # master msg
    # Receive from client or master in N-replicate process
    msg = socket.recv_pyobj()
    print("datakeeper rec")
    if msg["req"] == "upload":
        filename = msg['filename']
        if not os.path.exists('videos'):
            os.mkdir('videos')

        path = 'videos/' + filename
        video = msg['video']
        with open (path,"wb") as output:
            output.write(video)
        socket_master = context.socket(zmq.PUSH) 
        socket_master.bind("tcp://%s:8888" %str((data[0].split())[0]))
        socket_master.send_pyobj({'success': True, 'filename':filename})
        socket_master.close()

    elif msg["req"] == "download":
        filename = msg['filename']
        #video = open(order[1],'rb').read()
        #msg_to_client = {'filename': filename, 'video': video}
        #socket.send_pyobj(msg_to_client)


    
