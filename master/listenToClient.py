from sharedMemory import *
import zmq
import os

def listenToClient(socket):
    while True:
        # req_msg is like
        # req_msg = {'req': 'download', 'file_name': 'file.mp4', 'user_port': '5560'}
        # or
        # req_msg = {'upload','file.mp4'}
        req_msg = socket.recv_pyobj()
        # I am not sure h3ml eh be l node id l sra7a bs ktbah just in case
        if req_msg[0] == "upload":
            cond , node_data = getAvailableDataKeeper(req_msg[1])  # function to be implemented that
                        # checks on look-up table and sends id
                        # of first alive data keeper
                        # node_data is like {'ip': '127.0.0.1', 'port': '5555', node_id: 3}
            msg = "tcp://"+str(node_data['ip'])+":"+str(node_data['port'])
            socket.send_pyobj({"op":cond,"address":msg})
            #make Node port buzy
            lock.acquire()
            lookup[node_data]['busy']=True
            lock.release()

        elif req_msg['req'] == 'download':
            node_data = getNode(req_msg['file_name'])  # function to be implemented that
            # gets node of data keeper storing file_name
            msg = {'ip': node_data['ip'], 'port': node_data['port']}
            socket.send_pyobj(msg)


def getAvailableDataKeeper(file_name):
    # It will wait till it finds an alive data keeper and sends its ip
    while True:
        lock.acquire()
        for ip in lookup:
            if lookup[ip]['alive'] and not lookup[ip]['busy']:
                if file_name not in file_table.keys():
                    lock.release()
                    return "success" , ip
                else :
                    lock.release()
                    return "founded" , "tcp://000.0.0.0:0000"
                    
        lock.release()
        


def getNode(filename):
    # not sure if returning first data keeper having the file or we should randomize it
    lock.acquire()
    if filename in file_table:
        lock.release()
        return file_table[filename][0]


os.system("hostname -I >> ip.txt")
with open ("ip.txt", "r") as myfile:
    data=myfile.readlines()
i=sys.argv[1]
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://%s:%s"%data[0] %ports[i])
while True:
    listenToClient(socket)