import zmq
import sys
import os


# python3 datakeeper.py 6666

port = sys.argv[1]  # port of the datakeeper

context = zmq.Context()

socket = context.socket(zmq.PAIR)

os.system("hostname -I >> ip.txt")
os.system("hostname -I >> ip.txt")

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

ip = data[0].split()[0]
addr = "tcp://" + ip + ":" + port
socket.bind(addr)

socket_master = context.socket(zmq.PUSH)
master_address = "tcp://" + ip + ':' + str(int(port)+100)
socket_master.bind(master_address)

while True:
    # master msg
    # Receive from client or master in N-replicate process
    req = socket.recv_pyobj()
    print("req received from master")
    if req["req"] == "upload":
        filename = req['filename']
        path = str(port) + 'Videos'
        if not os.path.exists(path):
            os.mkdir(path)

        path = path + '/' + filename
        video = req['video']
        with open(path, "wb") as output:
            output.write(video)
        print("file is uploaded successfully")
        if req['checkWithMaster']:
            socket_master.send_pyobj({'success': True, 'filename': filename})

    elif req["req"] == "download":
        filename = req['filename']
        path = str(port) + 'Videos/' + filename
        video = open(path, 'rb').read()
        msg_to_client = {'filename': filename, 'video': video}
        print("sending video...")
        socket.send_pyobj(msg_to_client)
        print("file is sent")
        if req['checkWithMaster']:
            # To master to make dk not busy
            socket_master.send_string("done")
            print("msg sent to master to notify it's done")

