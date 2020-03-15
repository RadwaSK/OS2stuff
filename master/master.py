import threading
import zmq
from listenToClient import *

## SHARED DATA PART
lookup = {}
# file table will then store for each file,
# a list of id's for the data keepers saving that file
file_table = {}
lock = threading.Lock()

N = ## Number of Data keepers
# this list shall have
ports = list()
processes_num = int(sys.argv[1])
for i in range(processes_num):
    ports.append(i+5555)

for i in range(N):
    # i will act as the id of the data keeper
    ip_port = ## IP:port of a datakeeper
    # initially each id/data keeper will save its ip:port and it will be not alive
    # but then threads will update it with the received msgs from DataKeeperAlive
    lookup[ip_port] = {'id': i, 'alive': False, 'busy': False}
    # creating threads each listening to a port

    # There is something called thread.join() that would make the teh thread finish
    # its execution before the full code execution carries on.
    # I don't know if we're gonna need it, but just in case we do...

######################################################################################



## CHECKING DATA KEEPER ALIVE, and UPDATING LOOKUP
def resetAlive():
    lock.acquire()
    for ip in lookup:
        lookup[ip]['alive'] = False
    lock.release()


def listenToDataKeepers(socket):
    start = time.time()
    while True:
        msg = socket.recv_string()
        alive, ip = msg.split()
        lock.acquire()
        lookup[ip]['alive'] = True
        lock.release()
        if time.time() - start == 1:
            start = time.time()
            resetAlive()
####################################################



# Argv should be sth like this
# 'listener_to_alive_ip_port'

listener_to_alive_ip_port = sys.argv[1]

context = zmq.Context()
alive_socket = context.socket(zmq.SUB)
alive_socket.bind("tcp://%s" % listener_to_alive_ip_port)

# Supposedly by the time here, sharedMemory file is already executed
listener_thread = threading.Thread(target=listenToDataKeepers, name="alive_listener", args=(alive_socket,))
listener_thread.start()

client_listeners = []
listener_to_clients_ip_port = sys.argv[2]
N_clients = sys.argv[3]

requests_socket = context.socket(zmq.REP)
requests_socket.bind("tcp://%s" % listener_to_clients_ip_port)

for i in range(N_clients):
    client_listener = threading.Thread(target=listenToClient, name=str("client_listener#" + str(i)),
                                       args=(requests_socket,))
    client_listeners.append(client_listener)
    client_listener.start()
