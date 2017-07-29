
import os
import time
import zlib
import numpy as np
import sys
import cPickle as pickle
import json
import sys

import subprocess

processes = set()
max_processes = 10

alphas = [0.001, 0.01, 0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 1]
K = 20
# alphas = [0.5]
# K = 1

M = 20
no_epochs = 20000
lrate = 0.0008
command_list = []


for alpha in alphas:
	for index in range(K):
		cmd = 'OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python train_kink_apep.py -d ' \
			+ str(index) + ' -m ' + str(M) + ' -alpha ' + str(alpha) \
			+ ' -e ' + str(no_epochs) + ' -l ' + str(lrate)
		command_list.append(cmd)

for i, command in enumerate(command_list):
	print 'running', command
	processes.add(subprocess.Popen(command, shell=True))
	if len(processes) >= max_processes:
		os.wait()
		processes.difference_update([
			p for p in processes if p.poll() is not None])
		