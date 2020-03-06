from sharedMemory import *
import time


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
