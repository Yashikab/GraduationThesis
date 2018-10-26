import subprocess

#--set Num of Nodes--#
NODES = 6
INITIAL_PORT = 18400
PORT_LIST = []
for i in range(NODES):
    PORT_LIST.append(INITIAL_PORT+i)

for port in PORT_LIST:
    cmd = 'python3 Gilbert_nodes.py {p} &'.format(p=port)
    subprocess.run(cmd,shell=True)

    
