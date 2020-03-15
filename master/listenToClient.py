import zmq
import os


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
                    # The file already exists, so do nothing
                    lock.release()
                    return "founded" , "tcp://000.0.0.0:0000"
        lock.release()


def getNode(filename):
    # not sure if returning first data keeper having the file or we should randomize it
    lock.acquire()
    if filename in file_table:
        lock.release()
        return file_table[filename][0]
    else:
        lock.release()


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
    if req_msg[0] == "upload":
        cond, node_data = getAvailableDataKeeper(req_msg[1])  # function to be implemented that
        # checks on look-up table and sends id
        # of first alive data keeper
        # node_data is like {'ip': '127.0.0.1', 'port': '5555', node_id: 3}
        msg = "tcp://" + str(node_data)
        # send condition and address back to client
        socket.send_pyobj({"op": cond, "address": msg})
        # make Node port busy
        lock.acquire()
        lookup[node_data]['busy'] = True
        lock.release()

    elif req_msg['req'] == 'download': # TO DO
        node_data = getNode(req_msg['file_name'])  # function to be implemented that
        # gets node of data keeper storing file_name
        msg = {'ip': node_data['ip'], 'port': node_data['port']}
        socket.send_pyobj(msg)