import zmq 
import time
import os
import sys


# can run like that : python3 datakeeperAlive.py 6666

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

host_ip = data[0].split()[0]

port = sys.argv[1]

socket = zmq.Context().socket(zmq.PUB)
shift = int(port) % 13
ip_port = "tcp://" + host_ip + ":" + "5599"
socket.connect(ip_port)

while True:
    string = "alive " + host_ip + ':' + port
    socket.send_string(string)
    time.sleep(1)
