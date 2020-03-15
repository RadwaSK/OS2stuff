import zmq
import os

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


os.system("hostname -I >> ip.txt")

with open ("ip.txt", "r") as myfile:
    data = myfile.readlines()

i = sys.argv[1] # id of the process listening to client
context = zmq.Context()
socket = context.socket(zmq.REP) # type server
socket.bind("tcp://%s:%s"%data[0] %ports[i]) # Ports is from SharedMemory, data[0] is IP

while True:
    # receive order from client
    req_msg = socket.recv_pyobj()
    # I am not sure h3ml eh be l node id l sra7a bs ktbah just in case
    if req_msg['req'] == "upload":
        cond, node_data = getAvailableDataKeeper(req_msg['filename'])  # function to be implemented that
        # checks on look-up table and sends id
        # of first alive data keeper
        # node_data is like {'ip': '127.0.0.1', 'port': '5555', node_id: 3}
        address = "tcp://" + str(node_data)
        # send condition and address back to client
        socket.send_pyobj({"op": cond, "address": address})
        # make Node port busy
        lock.acquire()
        lookup[node_data]['busy'] = True
        lock.release()

    elif req_msg['req'] == 'download':
        cond, node_data = getNode(req_msg['file_name'])  # function to be implemented that
        # gets node of data keeper storing file_name
        address = "tcp://" + node_data
        msg = {'op': cond, 'address': address}
        # send ip:port back to client
        socket.send_pyobj(msg)
        # ANA M4 3MLA 7WAR L BUSY HERE YET!!