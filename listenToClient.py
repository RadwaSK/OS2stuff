import zmq
import sys
import time

def listenToClient(server_port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    ip = '127.0.0.1'
    socket.bind("tcp://" + ip + ':' + server_port)
    client_socket = context.socket(zmq.REQ)

    while True:
        # req_msg is like
        # req_msg = {'req': 'download', 'file_name': 'file.mp4', 'user_port': '5560'}
        req_msg = socket.recv_pyobj()
        # I am not sure h3ml eh be l node id l sra7a bs ktbah just in case
        if req_msg['req'] == 'upload':
            node_data = getAvailableDatakeeper() # function to be implemented that
                                            # checks on look-up table and sends id
                                            # of first alive data keeper
            # node_data is like {'ip': '127.0.0.1', 'port': '5555', node_id: 3}
            msg = {'ip': node_data['ip'], 'port': node_data['port']}
            client_socket.connect("tcp://" + ip + ':' + req_msg['user_port'])
            client_socket.send_pyobj(msg)
            client_socket.close()


        elif req_msg['req'] == 'download':
            node_data = getNode(req_msg['file_name']) # function to be implemented that
                                                # gets node of data keeper storing file_name
            msg = {'ip': node_data['ip'], 'port': node_data['port']}
            client_socket.connect("tcp://" + ip + ':' + req_msg['user_port'])
            client_socket.send_pyobj(msg)
            client_socket.close()
