import zmq
import sys
import os
import download
import upload



port= sys.argv[1]
context = zmq.Context()
socket = context.socket(zmq.REQ)

ip=open("host.txt",'r')
socket.bind("tcp://%s:%s" %ip %port)

while True :
    #master msg
    msg=socket.recv_pyobj()
    
