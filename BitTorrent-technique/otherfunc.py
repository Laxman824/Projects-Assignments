import socket
import sys
import hashlib
import threading
import time
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt


def splitLine(line):
	host = ""
	for i in range(0, len(line)):
		host += line[i]
		if(line[i+1] == '/'):
			break
	path = ""
	i+=1
	while(i<len(line)-1):
		path += line[i]
		if(line[i+1] == ','):
			break
		i+=1
	i+=2
	tcpConnections=""
	while(i<len(line)):
		tcpConnections +=line[i]
		i+=1
	tcp = int(tcpConnections)
	return host, path, tcp


def isHeaderDone(prev):
	if(prev[0] == '\r' and prev[1] == '\n' and prev[2] == '\r' and prev[3] == '\n'):
		return True
	return False

def updatLast4char(prev, data):
	prev.pop(0)
	prev.append(data)

def checkmd5sum(filename):
	obtainedmd5sum = hashlib.md5(open(filename, 'rb').read()).hexdigest()
	print("md5sum of downloaded file is : ", obtainedmd5sum)

