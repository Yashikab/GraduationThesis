import subprocess

for i in range(14):
	cmd = 'dot -Tpng test' + str(i) + '.dot -o test' + str(i) + '.png'
	subprocess.run(cmd,shell=True)