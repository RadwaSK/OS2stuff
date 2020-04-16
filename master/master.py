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
    j = i.split()
    for k in range(int(j[0])):
        ip_port = j[k+1] # IP:port of a datakeeper
        # initially each id/data keeper will save its ip:port and it will be not alive
        # but then threads will update it with the received msgs from DataKeeperAlive
        lookup[ip_port] = {'id': k, 'alive': True, 'busy': False}
    
    
######################################################################################

    # There is something called thread.join() that would make the the thread finish
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
    os.system("hostname -I >> ip.txt")
    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()

    ip = data[0].split()[0]
    context_alive = zmq.Context()
    socket_alive = context_alive.socket(zmq.SUB)
    socket_alive.bind("tcp://%s:5599" % ip)
    poller = zmq.Poller()
    poller.register(socket_alive, zmq.POLLIN)
    evts = poller.poll(100)
    socket_alive.setsockopt_string(zmq.SUBSCRIBE, "alive")
    counter = 0
    while True:
        msg = socket_alive.recv_string()
        counter += 1
        alive, ip = msg.split()
        lock.acquire()
        lookup[ip]['alive'] = True
        print(lookup)
        lock.release()
        if counter == len(lookup)-1:
            time.sleep(1)
            resetAlive()


################################################################
########################## listen to client ####################
def getAvailableDataKeeper(file_name):
    # It will wait till it finds an alive data keeper and sends its ip
    while True:
        lock.acquire()
        for ip in lookup:
            if lookup[ip]['alive'] and not lookup[ip]['busy']:
                if file_name not in file_table:
                    lock.release()
                    return "success", ip
                else:
                    # The file already exists, so do nothing
                    lock.release()
                    return "found", "000.0.0.0:0000"
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
    print("Start listening to clients, listener at port ", str(id+5555))

    if not os.path.isfile('ip.txt'):
        os.system("hostname -I >> ip.txt")

    with open("ip.txt", "r") as myfile:
        data = myfile.readlines()

    context = zmq.Context()
    socket = context.socket(zmq.REP)  # type server
    socket.bind("tcp://"+ (data[0].split())[0] +":"+str(id+5555)) # Ports is from SharedMemory, data[0] is IP

    while True:
        # receive order from client
        req_msg = socket.recv_pyobj()
        print("request received from client #", id)
        # I am not sure h3ml eh be l node id l sra7a bs ktbah just in case
        if req_msg['req'] == "upload":
            print("searching for datakeeper")
            cond, node_data = getAvailableDataKeeper(req_msg['filename'])
            if cond == 'found':
                print("file already exists")
                socket.send_pyobj({"op": cond, "address": node_data})
                continue
            
            print("datakeeper at ", node_data, " is free")
            print("sending address to client...")
            ip_port = node_data
            ip_port_list = node_data.split(":")
            ip = ip_port_list[0]
            port = ip_port_list[1]
            address = "tcp://" + str(ip_port)
            # send condition and address back to client
            socket.send_pyobj({"op": cond, "address": address})
            print("address is sent to client")
            # make Node port busy
            lock.acquire()
            lookup[node_data]['busy'] = True
            lock.release()
            #recieving ack from data keeper
            socket_data = context.socket(zmq.PULL) # type server
            dk_port = str(int(port) + 100)
            socket_data.connect("tcp://" + ip+ ':' + dk_port)
            print("connected to datakeeper")
            rec_msg = socket_data.recv_pyobj()
            print("acknowledgment is received from datakeeper")
            #{'success': True, 'filename': '1.mp4'}
            lock.acquire()
            file_table[rec_msg['filename']] = [ip_port]
            lookup[ip_port]['busy'] = False
            lock.release()
            socket_data.close()
            print("\n\n")

        elif req_msg['req'] == 'download':
            print("requesting downloading file: ", req_msg['filename'])
            # get the node that has this file
            print("searching for datakeeper having the file")
            cond, node_data = getNode(req_msg['filename'])
            if cond == 'not found':
                print("file not found on any datakeeper")
                msg = {'op': cond, 'address': node_data}
                socket.send_pyobj(msg)
                continue

            print("found in datakeeper: ", node_data)
            ip_port = node_data
            ip_port_list = node_data.split(":")
            ip = ip_port_list[0]
            port = ip_port_list[1]
            address = "tcp://" + ip_port
            msg = {'op': cond, 'address': address}
            # send ip:port back to client
            socket.send_pyobj(msg)
            print("address of datakeeper is sent back to client")
            # set this data keeper as busy since client will be downloading from it
            lock.acquire()
            lookup[ip_port]['busy'] = True
            lock.release()
            #recieving ack from data keeper
            socket_data = context.socket(zmq.PULL) # type server
            dk_port = str(int(port) + 100)
            socket_data.connect("tcp://" + ip +":" + dk_port)
            print("connected to datakeeper")
            rec_msg = socket_data.recv_string()
            print("acknowledgment is received from datakeeper")
            lock.acquire()
            lookup[node_data]['busy'] = False
            lock.release()
            socket_data.close()
            print("\n\n")


######################################################################
########################### N-Replicate ##############################
def getFreeIP(filename, dk):
    for dk_ip in lookup:
        if dk_ip == dk:
            continue
        if dk_ip not in file_table[filename] and lookup[dk_ip]['alive'] and not lookup[dk_ip]['busy']:
            return dk_ip
    return '0000.0.0.0'



def replicate():
    replicate_context = zmq.Context()
    start = time.time()
    while True:
        # I'll check every three seconds .. this is an assumption
        if time.time() - start == 3:
            lock.acquire()
            for file_name in file_table:
                # If it exists on less that three machines
                if len(file_table[file_name]) < 3:
                    # for each data keeper in file_table
                    for dk_ip in file_table[file_name]:
                        if lookup[dk_ip]['alive'] and not lookup[dk_ip]['busy']:
                            # get ip of a free dk that doesn't have the file
                            new_dk_ip = getFreeIP(file_name, dk_ip)
                            # if none found
                            if new_dk_ip == '0000.0.0.0':
                                break
                            # create a socket to get the file from data keeper
                            # type of socket is client
                            print("found a dk having the file")
                            dk_socket = replicate_context.socket(zmq.PAIR)
                            dk_socket.connect(str("tcp://" + dk_ip))
                            print("connected to it")
                            lookup[dk_ip]['busy'] = True
                            dk_socket.send_pyobj({'req': 'download', 'filename': file_name, "checkWithMaster": False})
                            print("sent request to dk")
                            # msg shall include the filename and the video itself
                            msg = dk_socket.recv_pyobj()
                            lookup[dk_ip]['busy'] = False
                            dk_socket.close()
                            # now connect to the free dk
                            dk_socket = replicate_context.socket(zmq.PAIR)
                            dk_socket.connect(str("tcp://" + new_dk_ip))
                            # sending video to it
                            dk_socket.send_pyobj({'req': 'upload', 'filename': msg['filename'], 'video': msg['video'], 'checkWithMaster': False})
                            dk_socket.close()
                            # add dk to list
                            file_table[file_name].append(new_dk_ip)
                            if len(file_table[file_name]) >= 3:
                                break
                    break
            lock.release()
            start = time.time()


############################################################################################
################################# ---- Main ---- ###########################################
# python3 master.py 3
listener_thread = threading.Thread(target=listenToDataKeepers, name="alive_listener")
listener_thread.start()
n = int(sys.argv[1])
for i in range(n):
    listen_to_client = threading.Thread(target=listen_2_client, name="client_listener",args=(int(i),))
    listen_to_client.start()

replicate_thread = threading.Thread(target=replicate, name="replicatesManager")
replicate_thread.start()
