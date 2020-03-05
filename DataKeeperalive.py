import zmq 
import time
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("IP_HOME")
parser.add_argument("IP_MASTER")
parser.add_argument("PORT")
args = parser.parse_args()

socket = zmq.Context().socket(zmq.PUB)
socket.connect("tcp://%s:5555" % args.IP_MASTER)

while True:
    socket.send_string("%s %s" % ("alive", str(args.IP_HOME+":"+args.PORT)))
    time.sleep(2)
