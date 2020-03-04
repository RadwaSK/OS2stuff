import zmq
import sys
import time
import os
import numpy as np

def sendAliveMsg(node_ip):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://%s:5555" %ip)
    socket.setsockopt_string(zmq.SUBSCRIBE, "alive")
    print(ip)
    while True:
        msg = socket.recv_string()
        topic, messagedata = msg.split()
        print(messagedata)



ip = sys.argv[1]
sendAliveMsg(ip)
