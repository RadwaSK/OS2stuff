from sharedMemory import *
import zmq

def listenToClient(socket):
    while True:
        # req_msg is like
        # req_msg = {'req': 'download', 'file_name': 'file.mp4', 'user_port': '5560'}
        # or
        # req_msg = {'req': 'upload', 'file_name': 'file.mp4', 'user_port': '5560'}
        req_msg = socket.recv_pyobj()
        # I am not sure h3ml eh be l node id l sra7a bs ktbah just in case
        if req_msg['req'] == 'upload':
            node_data = getAvailableDataKeeper()  # function to be implemented that
                        # checks on look-up table and sends id
                        # of first alive data keeper
                        # node_data is like {'ip': '127.0.0.1', 'port': '5555', node_id: 3}
            msg = {'ip': node_data['ip'], 'port': node_data['port']}
            socket.send_pyobj(msg)

        elif req_msg['req'] == 'download':
            node_data = getNode(req_msg['file_name'])  # function to be implemented that
            # gets node of data keeper storing file_name
            msg = {'ip': node_data['ip'], 'port': node_data['port']}
            socket.send_pyobj(msg)


def getAvailableDataKeeper():
    # It will wait till it finds an alive data keeper and sends its ip
    while True:
        for ip in lookup:
            if lookup[ip]['alive']:
                return ip


def getNode(filename):
    # not sure if returning first data keeper having the file or we should randomize it
    if filename in file_table:
        return file_table[filename][0]
