def upload(ip_port, socket):
    # the ip_port is for the data keeper saving the file
    msg = socket.recv_pyobj()
    filename = msg['filename']
    video = msg['video']

    # TO DO!
    # save the file or something?

    lock.acquire()
    # This is the first time to store an object, so I make the key in dictionary and set
    # the value to an array with data keeper ip_port .. in replicate, I'd append to it
    file_table[filename] = [ip_port]
    lock.release()
