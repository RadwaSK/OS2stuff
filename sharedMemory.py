import sys
import threading

# Argv should be sth like this
# '*:5000' '3' '127.0.0.1:5001' '192.168.58.255:5002' '127.0.0.1:5003'

lookup = {}
# file table will then store for each file,
# a list of id's for the data keepers saving that file
file_table = {}
lock = threading.Lock()

N = int(sys.argv[2])
# this list shall have
ports = []

for i in range(N):
    # i will act as the id of the data keeper
    ip_port = sys.argv[i+2]
    # initially each id/data keeper will save its ip:port and it will be not alive
    # but then threads will update it with the received msgs from DataKeeperAlive
    lookup[ip_port] = {'id': i, 'alive': False, 'busy': False}
    # creating threads each listening to a port

    # There is something called thread.join() that would make the teh thread finish
    # its execution before the full code execution carries on.
    # I don't know if we're gonna need it, but just in case we do...

