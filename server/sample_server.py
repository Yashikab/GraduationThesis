import socket
from datetime import datetime
import sys
import pickle as pkl
#--How to run--#
#$python3 sample_client.py [PORT]
MAX_SIZE = 1024

argvs = sys.argv
argc = len(argvs)
if (argc < 2):
    print ('You have to add [PORT] like "python3 sample_client.py [####]"')
    sys.exit()

#--address&port--#
HOST = 'localhost'
PORT = int(argvs[1])
address = (HOST,PORT)

#--starting server--#
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(address)
server.listen(10) #waiting for client

#--get info from client--#
print('Waiting for connection...')
client_sock, client_addr = server.accept()
#client_sock.send(b"server : connection start \n\n")


while True:
    b_msg = client_sock.recv(MAX_SIZE)
    #msg = msg.rstrip()
    msg = pkl.loads(b_msg)

    print ('Received -> %s'  % msg)

    if msg == 'quit':
        client_sock.send(pkl.dumps("server : connection end \n\n"))
        print('connection end')
        break
    elif msg == 'continue':
        client_sock.send(pkl.dumps('Go ahead!'))
        b_msg2 = client_sock.recv(MAX_SIZE)
        #msg = msg.rstrip()
        msg2 = pkl.loads(b_msg2)
        print ('Received -> %s'  % msg2)
        print('Type Message ...')
        str_msg = input()
        s_msg = pkl.dumps(str_msg)
        client_sock.send(s_msg)

    else:
        print('Type Message ...')
        str_msg = input()
        s_msg = pkl.dumps(str_msg)
        client_sock.send(s_msg)


client_sock.close()
server.close()
