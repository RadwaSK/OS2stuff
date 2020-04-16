import zmq
import sys
import os
import time
import threading
import logging





def leader(port , context ):
    print("I'm the new Leader.")
    mysocket = context.socket(zmq.REP)
    
    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()

    mysocket.bind("tcp://"+str((data[0].split())[0])+":"+port)

    while True:
        msg = mysocket.recv_string()
        mysocket.send_string("Leader with number "+ port +" is here.")
        print("I'm the Leader.")



def process(port , context):
    global leaderport
    mysocket = context.socket(zmq.REQ)
    mysocket.RCVTIMEO = 500 #assume we have the overhead of the network

    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()
    mysocket.connect("tcp://"+str((data[0].split())[0])+":"+str(leaderport))

    while True :
        mysocket.send_string("process number "+ port +" is here.")
        try:
            msg = mysocket.recv_string()
            print(msg)
            time.sleep(5)
        except :
            mysocket.disconnect("tcp://"+str((data[0].split())[0])+":"+str(leaderport))
            mysocket.close()
            election(port , context)


def replyer (port , context ):
    #logging.info( "replyer thread is working")
    print ( "replyer thread is working")
    mysocket = context.socket(zmq.REP)
    mysocket.RCVTIMEO = 50 #small to get the update of elec_bool very quick

    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()
    mysocket.bind("tcp://"+str((data[0].split())[0])+":"+port)
    while True:
        global elec_bool
        if not elec_bool :
            try:
                msg = mysocket.recv_string()
                print("replyer recived from "+msg)
                mysocket.send_string(port + " "+ str(leaderport))
            except :
                pass
        else: 
            mysocket.unbind("tcp://"+str((data[0].split())[0])+":"+port)
            mysocket.close()
            break
    print("replyer is ended")
    return 
    
def checkleader ( ports , context , port , direction):
    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()
    try:
        mysocket = context.socket(zmq.REQ)
        mysocket.RCVTIMEO = 100
        #try to connect to the leader port
        mysocket.connect("tcp://"+str((data[0].split())[0])+":"+ports.split()[1])
        print ( "i try sent to Leader")
        mysocket.send_string(port)
        print ("success sending ... ")
        msg = mysocket.recv_string()
        if msg.split()[0] == "Leader" :
            mysocket.disconnect("tcp://"+str((data[0].split())[0])+":"+ports.split()[1])
            mysocket.close()
            return msg.split()[3]

    except :
        mysocket.disconnect("tcp://"+str((data[0].split())[0])+":"+ports.split()[1])
        mysocket.close()
        if direction == "up":
            return ports.split()[0]
        else : 
            return port





def election(port , context) :
  
    with open ("ip.txt", "r") as myfile:
        data = myfile.readlines()
    global leaderport
    global elec_bool
    for i in range (9999-int (port)):
        try:
            mysocket = context.socket(zmq.REQ)
            mysocket.RCVTIMEO = 200
            msg = ""
            mysocket.connect("tcp://"+str((data[0].split())[0])+":"+str(9999-i))
            print ( "i try sent to " + str(9999-i))
            mysocket.send_string(port)
            print ("success sending ... ")
            msg += mysocket.recv_string()
            print ("recived msg " + msg)
            # we have 2 cases 
            # one of them is all of us electing
            # second one process was sleeping then wakeup after election 
            if msg.split()[0] == "Leader" :
                mysocket.disconnect("tcp://"+str((data[0].split())[0])+":"+str(9999-i))
                mysocket.close()
                time.sleep(0.25)
                
                leaderport = int(msg.split()[3])
                process(port  , context)
            else :
                mysocket.disconnect("tcp://"+str((data[0].split())[0])+":"+str(9999-i))
                mysocket.close()
                
                leaderport =int(checkleader(msg , context , port , "up"))
                time.sleep(0.25)
                process(port , context)
        except :
            print ( "fialled  sent to " + str(9999-i))
            mysocket.close()
    #max number of machines = 20
    for i in range (1,10):
        try:
            mysocket = context.socket(zmq.REQ)
            mysocket.RCVTIMEO = 20
            msg = ""
            mysocket.connect("tcp://"+str((data[0].split())[0])+":"+str(int (port)-i))
            print ( "i try sent to " + str(int (port)-i))
            mysocket.send_string(port)
            print ("success sending ... ")
            msg += mysocket.recv_string()
            print ("recived msg " + msg)
            # we have 2 cases 
            # one of them is all of us electing
            # second one process was sleeping then wakeup after election 
            if msg.split()[0] == "Leader" :
                mysocket.disconnect("tcp://"+str((data[0].split())[0])+":"+str(int (port)-i))
                mysocket.close()
                time.sleep(0.25)
                
                leaderport = int(msg.split()[3])
                process(port , context)
            else :
                mysocket.disconnect("tcp://"+str((data[0].split())[0])+":"+str(int (port)-i))
                mysocket.close()
                
                leaderport =int(checkleader(msg , context , port , "down"))
                if int(port) != leaderport : 
                    time.sleep(0.25)
                    process(port  , context)
                else :
                    elec_bool = True
                    th.join()
                    leader(port , context)
        except :
            print ( "fialled  sent to " + str(int (port)-i))
            mysocket.close()



    
    elec_bool = True
    th.join()
    leader(port , context)






port = str (sys.argv[1])

elec_bool = False
leaderport = 9999
context = zmq.Context()
os.system("hostname -I >> ip.txt")
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

th = threading.Thread(target=replyer, args=(port, context, ))
th.start()
process(port, context)
    
