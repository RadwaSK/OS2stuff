from sharedMemory import *
import zmq


def upload(ip_port, socket):
    # ip_port is for the user requesting the file

    # TO DO
    # video = ...
    # construct msg
    msg = {}
    socket.send_pyobj(msg)


