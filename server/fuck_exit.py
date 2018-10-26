import sys
sys.path.append('./module')

import socket
from datetime import datetime as dt
import pickle as pkl
#import Gilbert as gl
import pandas as pd
import numpy as np
import math
import time
#--initial definition--#
MAX_SIZE = 4096

def recvall(sock):
    data = b''
    while True:
        part = sock.recv(MAX_SIZE)
        data += part
        if len(part) < MAX_SIZE:
            break
    return data

#--address&port--#
HOST = 'localhost'
NODES = 30
PORT_LIST = []
for PORT in range(18400,18400+NODES):
    PORT_LIST.append(PORT)


#--access to each server--#
address = []
client = []
for PORT in PORT_LIST:
    address.append((HOST,PORT))
    client.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))

#--send dataset--#
for i in range(NODES):
    client[i].connect(address[i])
    client[i].sendall(b'end') #protocol

