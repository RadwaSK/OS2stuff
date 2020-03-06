import threading
import zmq
from listenToClient import *
from checkAlive import *

# Argv should be sth like this
# 'listener_to_alive_ip_port' 'listener_to_clients_ip_port' 'N_clients'

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
