import zmq
import sys
import time
from multiprocessing import shared_memory

sec = sys.argv[1]
table =shared_memory.SharedMemory("data_keepers")
files=shared_memory.SharedMemory("files")
while True:
    time.sleep(sec)
    print("table",table)
    print("files",files)
    files.close()   
    table.close()
