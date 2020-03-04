import zmq
import sys
import time
import os
import numpy as np

def receive_alive_Msg(master_ip,num_of_nodes):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.RCVTIMEO = 100
    socket.bind("tcp://%s:5555" %master_ip)
    socket.setsockopt_string(zmq.SUBSCRIBE, "alive")
    i=0
    while i<num_of_nodes:#only until know
        msg = socket.recv_string()
        topic, messagedata = msg.split()
        print(messagedata)



ip = sys.argv[1]
num_of_nodes = sys.argv[2]
receive_alive_Msg(ip,num_of_nodes)
