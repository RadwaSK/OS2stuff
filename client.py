import zmq
import sys
import time


def upload():





def download():
    
ip = sys.argv[1]
port = sys.argv[2]

while True :
    order = input ("enter your order :")
    order = order.split()
    if order[0]=="upload":
        upload()
    else if order[0]=="download":
        download()