import zmq
import sys
import time
import os
import numpy as np
from multiprocessing import shared_memory

def receive_alive_Msg(master_ip,num_of_nodes,table,files):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.RCVTIMEO = 100
    socket.bind("tcp://%s:5555" %master_ip)
    socket.setsockopt_string(zmq.SUBSCRIBE, "alive")
    i=0
    #while i<num_of_nodes:#only until know
     #   msg = socket.recv_string()
      #  topic, messagedata = msg.split()
       # print(messagedata)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        files.close()   
        table.close()
        files.unlink()
        table.unlink()

def lock_up ():
    f=list()
    d=list()
    for i in range(100):
        name=""
        id_list="0"
        f.append(name)
        f.append(id_list)
    for i in range(20):
        ip="000.0.0.1"
        port="0000"
        live=False
        busy=False
        d.append(ip)
        d.append(port)
        d.append(live)
        d.append(busy)

    table = shared_memory.SharedMemory(name ="data_keepers",create=True, size=sys.getsizeof(d))
    files = shared_memory.SharedMemory(name ="files",create=True, size=sys.getsizeof(f))
    return table,files



ip = sys.argv[1]
num_of_nodes = sys.argv[2]
table,files=lock_up()
receive_alive_Msg(ip,num_of_nodes,table,files)
