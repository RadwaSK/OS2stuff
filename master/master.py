import threading
import zmq
import time
import os
import sys 
################################ SHARED DATA PART #################################
lookup = {}
# file table will then store for each file,
# a list of id's for the data keepers saving that file
file_table = {}
lock = threading.Lock()

with open ("dk_ips.txt", "r") as myfile:
    data = myfile.readlines()
for i in data:
    j=i.split()
    for k in range(int(j[0])):
        ip_port =j[1]+":"+str(k+6666) # IP:port of a datakeeper
        # initially each id/data keeper will save its ip:port and it will be not alive
        # but then threads will update it with the received msgs from DataKeeperAlive
        lookup[ip_port] = {'id': i, 'alive': False, 'busy': False}

######################################################################################

    # There is something called thread.join() that would make the teh thread finish
    # its execution before the full code execution carries on.
    # I don't know if we're gonna need it, but just in case we do...

############### CHECKING DATA KEEPER ALIVE, and UPDATING LOOKUP ######################
def resetAlive():
    lock.acquire()
    for ip in lookup:
        lookup[ip]['alive'] = False
    lock.release()


def listenToDataKeepers():
    os.system("hostname -I >> ip.txt")
    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()
    context_alive = zmq.Context()
    socket_alive = context_alive.socket(zmq.SUB)
    socket_alive.bind("tcp://%s:5599" % data[0])
    poller = zmq.Poller()
    poller.register(socket_alive, zmq.POLLIN)
    evts = poller.poll(100)
    socket_alive.setsockopt_string(zmq.SUBSCRIBE, "alive")
    counter = 0
    while True:
        msg = socket_alive.recv_string()
        counter+=1
        alive, ip = msg.split()
        lock.acquire()
        lookup[ip]['alive'] = True
        print(lookup)
        lock.release()
        if counter == len(lookup)-1:
            time.sleep(1)
            resetAlive()
####################################################

########################## listen to client ####################
def getAvailableDataKeeper(file_name):
    # It will wait till it finds an alive data keeper and sends its ip
    while True:
        lock.acquire()
        for ip in lookup:
            if lookup[ip]['alive'] and not lookup[ip]['busy']:
                if file_name not in file_table:
                    lock.release()
                    return "success" , ip
                else :
                    # The file already exists, so do nothing
                    lock.release()
                    return "founded" , "000.0.0.0:0000"
        lock.release()


def getNode(filename):
    # not sure if returning first data keeper having the file or we should randomize it
    lock.acquire()
    if filename in file_table.keys():
        # waiting till I find a not-busy and alive datakeeper from those having the file
        while True:
            # looping on list of data keepers having this file
            for ip_port in file_table[filename]:
                if lookup[ip_port]['alive'] and not lookup[ip_port]['busy']:
                    lock.release()
                    return 'found', ip_port
    else:
        lock.release()
        return 'not found', '000.0.0.0:000'

def listen_2_client(id):
    if not os.path.isfile('ip.txt'):
        os.system("hostname -I >> ip.txt")

    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()

    context = zmq.Context()
    socket = context.socket(zmq.REP) # type server
    socket.bind("tcp://"+ (data[0].split())[0] +":"+str(id+5555)) # Ports is from SharedMemory, data[0] is IP

    while True:
        # receive order from client
        req_msg = socket.recv_pyobj()
        # I am not sure h3ml eh be l node id l sra7a bs ktbah just in case
        if req_msg['req'] == "upload":
            cond, node_data = getAvailableDataKeeper(req_msg['filename'])  # function to be implemented that
            # checks on look-up table and sends id
            # of first alive data keeper
            address = "tcp://" + str(node_data)
            # send condition and address back to client
            socket.send_pyobj({"op": cond, "address": address})
            # make Node port busy
            lock.acquire()
            lookup[node_data]['busy'] = True
            lock.release()
            #recieving ack from data keeper
            socket_data = context.socket(zmq.PULL) # type server
            socket_data.connect("tcp://" + (node_data.split(':'))[0]+":8888")
            rec_msg = socket_data.recv_pyobj()
            #{'success': True, 'filename': '1.mp4'}
            lock.acquire()
            file_table[rec_msg['filename']]=list(lookup[node_data]['id'])
            lookup[node_data]['busy'] = False
            lock.release()

        elif req_msg['req'] == 'download':
            # get the node that has this file
            cond, node_data = getNode(req_msg['file_name'])
            address = "tcp://" + node_data
            msg = {'op': cond, 'address': address}
            # send ip:port back to client
            socket.send_pyobj(msg)
            # set this data keeper as busy since client will be downloading from it
            lock.acquire()
            lookup[node_data]['busy'] = True
            lock.release()
            # create another socket to receive from data keeper
            dk_socket = context.socket(zmq.PULL) # type PULL
            dk_socket.connect(address)
            # This is done to know that the downloading is done
            m_dummy = dk_socket.recv_pyobj()
            lock.acquire()
            lookup[node_data]['busy'] = False
            lock.release()
            dk_socket.close()

######################################################################
# python3 master.py 3
# Supposedly by the time here, sharedMemory file is already executed
listener_thread = threading.Thread(target=listenToDataKeepers, name="alive_listener")
listener_thread.start()
n=int(sys.argv[1])
for i in range(n):
    listen_to_client = threading.Thread(target=listen_2_client, name="client_listener",args=(int(i),))
    listen_to_client.start()