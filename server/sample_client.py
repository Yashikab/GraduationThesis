import socket
from datetime import datetime
import sys
import pickle as pkl
#--How to run--#
#$python3 sample_client.py [HOST] [PORT]
MAX_SIZE = 1024*4

#argvs = sys.argv
#argc = len(argvs)
#if (argc < 3):
#    print('You have to add [HOST][PORT] like "python3 sample_client.py localhost [####]"')

def talk(client):
    while True:
        response = client.recv(MAX_SIZE)
        print(response)
        #load_msg = pkl.loads(response)
        print ('Server said: %s' % response)

        print("Send Message:" )
        str_msg = input()
        if(str_msg == 'continue'):
            s_msg = pkl.dumps(str_msg)
            client.send(s_msg)
            resp = client.recv(MAX_SIZE)
            client.send(pkl.dumps('Fuck YOU!'))
        else:
            s_msg = pkl.dumps(str_msg)
            client.send(s_msg)

        if str_msg == 'quit':
            break




#--address&port--#
HOST = 'localhost'
PORT_LIST = [18400,18401]
address = []
client = []
for PORT in PORT_LIST:
    address.append((HOST,PORT))
    client.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))

start_msg = 'Connection Started'
for i in range(len(PORT_LIST)):
    client[i].connect(address[i])
    client[i].send(pkl.dumps(start_msg))

talk(client[0])
talk(client[1])




#client.close()
 