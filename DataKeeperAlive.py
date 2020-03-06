import zmq 
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("IP_HOME")
parser.add_argument("IP_MASTER")
parser.add_argument("PORT_MASTER")
parser.add_argument("PORT")
args = parser.parse_args()

socket = zmq.Context().socket(zmq.PUB)
ip_port = "tcp://" + args.IP_MASTER + ":" + args.PORT_MASTER
socket.connect(ip_port)

while True:
    socket.send_string("%s %s" % ("alive", str(args.IP_HOME+":"+args.PORT)))
    time.sleep(1)
