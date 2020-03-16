import zmq
import sys
import time


def replicate():
    start = time.time()
    while True:
        # I'll check every three seconds .. this is an assumption
        if time.time() - start == 3:
            lock.acquire()
            for file in file_table:
                # If it exists on less that three machines
                if len(file_table[file]) < 3:
                    # for each data keeper in file_table
                    for datakeeper in file_table[file]:
                        if lookup[datakeeper]['alive'] and not lookup[datakeeper]['busy']:
                            # create a socket to get the file from data keeper
                            # type of socket is client
                            dk_socket = context.socket(zmq.REQ)
                            dk_socket.connect(str("tcp://" + datakeeper))
                            dk_socket.send_pyobj({'req': 'download', 'filename': file})
                            # msg shall include the filename and the video itself
                            msg = dk.socket.recv_pyobj()
                            dk_socket.close()
                            num_of_devices = len(file_table[file])
                            for new_datakeeper in lookup:
                                # if the datakeeper doesn't have the file
                                if new_datakeeper not in file_table[file]:
                                    dk_socket.connect(str("tcp://" + new_datakeeper))
                                    dk_socket.send_pyobj({'req': 'upload', 'filename': msg['filename'],
                                                          'video': msg['video']})
                                    ''' This is to be un-commented IFF you made dk send a verification msg
                                     or whatever after upload is successfully done
                                     which I think we should since dk_address is server, and I'm a client here
                                     Check the comment in the ddatakeeper file '''
                                    # msg = dk_socket.recv_pyobj()
                                    dk_socket.close()
                                    num_of_devices += 1
                                if num_of_devices == 3:
                                    break
                            break

            lock.release()
            start = time.time()
