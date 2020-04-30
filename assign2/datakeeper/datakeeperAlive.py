import zmq 
import time
import os
import sys


# can run like that : python3 datakeeperAlive.py 6666

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

my_ip = data[0].split()[0]

host_ip = sys.argv[1]
port = sys.argv[2]

socket = zmq.Context().socket(zmq.PUB)
shift = int(port) % 13
ip_port = "tcp://" + host_ip + ":" + "5599"
socket.connect(ip_port)

while True:
    #string = "alive " + my_ip + ':' + port
    string = "alive " + my_ip
    socket.send_string(string)
    time.sleep(1)
