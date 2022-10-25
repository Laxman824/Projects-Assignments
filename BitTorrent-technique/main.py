#!/usr/bin/env python
import socket
import sys
import hashlib
import threading
from threading import Lock
import time
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt 
import otherfunc

#globally defined
host = []
path = []
tcps = []
port = 80
chunkSize = 10240 #10KB
chunks = []
i=0
totalBytes = int(sys.argv[3]) #given file size
while(i < totalBytes):
	chunks.append((i, min(totalBytes-1, i+chunkSize-1)))
	i += chunkSize
totalChunks = len(chunks)
totalThreads = 0
executedTotal = [0]*totalThreads
timeTaken = [0.0]*totalThreads
downloadedParts = [""]*totalChunks
isVisited = [False]*totalChunks

def DrawPlot():
	fig = plt.figure()
	plt.title(f"Relation in Time and total downloaded chunks by all threads")
	plt.xlabel("downloaded chunks")
	plt.ylabel("Time taken (in sec)")
	for i in range(0, totalThreads):
		X = []
		for j in range(0, len(timeTaken[i])):
			X.append(len(X)+1)
		plt.plot(X, timeTaken[i], label=f"thread-{i}")
	plt.legend()
	plt.savefig(f"myPlot.png")
	plt.close()

def getHost(threadID):
	h = host[0]
	p = path[0]
	tcps[0]-=1
	if(tcps[0] ==0):
		host.pop(0)
		path.pop(0)
		tcps.pop(0)
	return h, p

class myThread (threading.Thread):
   def __init__(self, threadID, name, hostID):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.hostID = hostID
   def run(self):
      print("Starting " + self.name)
      downloadData(self.name, self.threadID, self.hostID)
      print("Exiting " + self.name)

def downloadData(threadName, threadID, hostID):
	timetaken = []
	chunksDownloaded = []
	i = threadID
	cnt = 0
	host1 = hostID[0]
	path1 = hostID[1]
	print(f"establishing a new tcp connection for {threadName}")
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			print(f"hand-shaking the tcp connection {threadName}")
			clientSocket.connect((host1, port))
			break
		except:
			print(f"Unable to hand-shake, retrying {threadName}")
	sTime = time.clock()
	while(i<totalChunks):
		currChunk = chunks[i]
		command = f"GET {path1} HTTP/1.1\r\nHost:{host1}\r\nConnection:keep-alive\r\nRange: bytes={currChunk[0]}-{currChunk[1]}\r\n\r\n"
		clientSocket.sendall(command.encode())
		count = 0
		start = False
		prev = ['a', 'a', 'a', 'a']
		j=0
		string = ""
		header = ""
		success = True
		
		while count < currChunk[1]-currChunk[0]+1:
			recev = True
			while True:
				try:
					data = clientSocket.recv(1)
					break
				except:
					recev = False
					break
			j=j+1
			if not data or not recev:
				print(f"Data not received in {threadName}")
				success = False
				recev = True
				break
			if(start):
				string += data.decode()
				count = count+1
				continue
			header += data.decode()
			otherfunc.updatLast4char(prev, data.decode())
			start = otherfunc.isHeaderDone(prev)
		if(not success): #internet connection closed
			clientSocket.close()
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			while True:
				try:
					clientSocket.connect((host1, port))
					break
				except:
					print(f"Unable to rehand-shake, retrying {threadName}")
			continue
		cnt+=1
		executedTotal[threadID]+=1
		isVisited[i] = True
		downloadedParts[i] = string
		print("downloaded chunk: ", i)
		i+=totalThreads
		chunksDownloaded.append(cnt)
		timetaken.append(time.clock()-sTime)
		# when max limit of requests for a tcp connection reached
		if(header.find('Connection: close') != -1): 
			clientSocket.close()
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			while True:
				try:
					clientSocket.connect((host1, port))
					break
				except:
					print(f"Unable to rehand-shake, retrying {threadName}")
	timeTaken[threadID] = timetaken
	clientSocket.close()


def initialization():
	global executedTotal
	global timeTaken
	global downloadedParts
	global isVisited
	executedTotal = [0]*totalThreads
	timeTaken = [None]*totalThreads
	for i in range(0, totalChunks):
		downloadedParts[i] = "" #initialization
	isVisited = [False]*totalChunks

def DownloadFile():
	initialization()
	allthreads = []
	for i in range(0, totalThreads):
		h,p = getHost(i)
		thread = myThread(i, f"Thread-{i}", (h,p))
		allthreads.append(thread)

	for i in range(0, totalThreads):
		allthreads[i].start()
	for t in allthreads:
		t.join()

	print("Saving file")
	filename = sys.argv[2]
	file1 = open(filename, "w")
	for i in range(0,totalChunks):
		file1.write(downloadedParts[i])
	file1.close()
	print("total number of chunks executed by each Thread:")
	for i in range(0, totalThreads):
		print(f"thread-{i} ", executedTotal[i])
	otherfunc.checkmd5sum(filename)
	print("File downloaded")

def ReadInput():
	input = open(sys.argv[1], "r")
	i=1
	line = input.readline()
	print(line)
	global totalThreads
	totalThreads=0
	while line != "":	
		host1, path1, totalThreads1 = otherfunc.splitLine(line)
		global host
		global path
		global tcps
		host.append(host1)
		path.append(path1)
		tcps.append(totalThreads1)
		totalThreads += totalThreads1
		line = input.readline()
	DownloadFile();


ReadInput()
DrawPlot()
