import zmq 
import time
import os
import sys


# can run like that : python3 datakeeperAlive.py 1 6666 3

os.system("hostname -I >> ip.txt")
os.system("hostname -I >> ip.txt")

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

indx = int(sys.argv[1])
my_ip = data[0].split()[indx]

master_ip = data[0].split()[0]
first_port = int(sys.argv[2])
n_ports = int(sys.argv[3])

socket = zmq.Context().socket(zmq.PUB)
# shift = int(port) % 13
ip_port = "tcp://" + master_ip + ":" + "5599"
socket.connect(ip_port)

while True:
    # string = "alive " + my_ip + ':' + port
    for i in range(n_ports):
        string = "alive " + my_ip + ':' + str(first_port+i)
        socket.send_string(string)
    time.sleep(3)
