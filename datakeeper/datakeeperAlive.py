import zmq 
import time
import os
import sys

# can run like that : python3 DataKeeperAlive.py 192.168.1.2 1


with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

host_ip = data[0].split()[0]

num_proccess=int (sys.argv[1])

socket = zmq.Context().socket(zmq.PUB)
ip_port = "tcp://" + host_ip + ":" + "5599"
socket.connect(ip_port)

while True:
    for i in range(num_proccess):
        socket.send_string("%s %s" % ("alive",str((data[0].split())[0])+":"+str(i+6666)))
    time.sleep(1)
