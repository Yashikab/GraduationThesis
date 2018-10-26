import sys
sys.path.append('../module')
sys.path.append('../cpp_module')
import socket
from datetime import datetime
import pickle as pkl
import Gilbert as gl
import pandas as pd
import numpy as np
import math
import distbasic as basic

#--How to run--#
#$python3 sample_server.py [PORT]
MAX_SIZE = 4096
class2 = False

argvs = sys.argv
argc = len(argvs)
if (argc < 2):
    print ('You have to add [PORT] like "python3 sample_server.py [####]"')
    sys.exit()

#--address&port--#
HOST = 'localhost'
PORT = int(argvs[1])
address = (HOST,PORT)

#--starting server--#
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(address)
server.listen(10) #waiting for client

while True:
    #--get info from client--#
    print('PORT: %d \tWaiting for connection...' % PORT)
    client_sock, client_addr = server.accept()
    #--greeting--#
    greeting_msg = client_sock.recv(MAX_SIZE)
    if greeting_msg == b'quit':
        print('PORT: %d \tserver close' % PORT)
        break
    elif greeting_msg == b'hello':
        client_sock.sendall(greeting_msg)
        class2 = False
    elif greeting_msg == b'2class':
        client_sock.sendall(greeting_msg)
        class2 = True
    else:
        print('PORT: %d \tError has occured!')
        sys.exit

    print('PORT: %d \tconnection started' % PORT)

    #--step i--#
    counter = 0

    while True:
        
        #print('waiting')
        rcv_msg = client_sock.recv(MAX_SIZE)
        #print(rcv_msg)
        #--get dataset--#
        if rcv_msg == b'dataset':
            print('PORT: %d \treceive dataset' % PORT)
            client_sock.sendall(b'goahead')
            #--get dataset--#
            b_data = gl.recvall(client_sock) #get dataset
            set_P = pkl.loads(b_data) #get dataset
            client_sock.sendall(b'done')
            DIM = len(set_P[0]) - 1
            if class2:
                set_A = []
                set_B = []
                for data in set_P:
                    if data[DIM] == 1:
                        set_A.append([data[d] for d in range(DIM)])

                    elif data[DIM] == -1:
                        set_B.append([data[d] for d in range(DIM)])
                set_A = np.array(set_A)
                set_B = np.array(set_B)
                print(len(set_A),len(set_B))
                # print(set_B)
                basic.datalen(len(set_A), len(set_B))
                basic.inputdata(set_A.tolist(), set_B.tolist())
            print('receive dataset: Done!')

        #--step 1--#
        elif rcv_msg == b'step1':
            # print('PORT: %d \trunning step: 1' % PORT)
            counter = 1
            if class2:
                client_sock.sendall(b'goahead')
                b_x11 = gl.recvall(client_sock)
                x11 = pkl.loads(b_x11)
                dist_list = basic.l2list(x11.tolist(), 1)
                x21 = set_B[np.argmin(dist_list)]
                b_x21 = pkl.dumps(x21)
                client_sock.sendall(b_x21)
            else:
                #--step 1--#
                x1 = gl.minDistP(set_P)
                b_x1 = pkl.dumps(x1)
                client_sock.sendall(b_x1)
            # print('step1: Done!')
                



        #--step i--#
        elif rcv_msg == b'stepi':
            counter += 1
            # print('PORT: %d \trunning step: %d' % (PORT,counter))
            client_sock.sendall(b'goahead')
            #get x
            b_x = gl.recvall(client_sock)
            if class2:
                x1,x2,flag = pkl.loads(b_x)
                if flag == 'A':
                    # newP = gl.PbarX_Min(x2,x1,set_A)
                    PbarX_list1 = basic.dotlist(x2.tolist(), x1.tolist(),0)
                    g_1i = np.min(PbarX_list1)
                    p_1i = set_A[np.argmin(PbarX_list1)]
                    newP = [p_1i, g_1i]
                    
                elif flag == 'B':
                    # newP = gl.PbarX_Min(x1,x2,set_B)
                    PbarX_list2 = basic.dotlist(x1.tolist(), x2.tolist(),1)
                    g_2i = np.min(PbarX_list2)
                    p_2i = set_B[np.argmin(PbarX_list2)]
                    newP = [p_2i, g_2i]

            else:
                x = pkl.loads(b_x)

                #calc PbarX
                if class2:
                    newP = gl.PbarX2(x, set_P)
                else:
                    newP = gl.PbarX(x, set_P)

            #send newP
            b_newP = pkl.dumps(newP)
            client_sock.sendall(b_newP)

        elif rcv_msg == b'end':
            print('PORT: %d \tSession completed!' % PORT)
            break

        else:
            print('PORT:%d \tProtcol error has occerd!' % PORT)
            break


    client_sock.close()

   
