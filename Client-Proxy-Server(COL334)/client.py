import socket
import sys
#this function returns a string to send the information to the server.
#string : filename + '\n' + (sequence of host, port from 2nd proxy to the server)
def createRequest(filename, servers):
	req_sent = filename+"\n"
	for i in range(1, len(servers)):
		req_sent += servers[i]+'\n'
	return req_sent
	
#readInput read the input file and separate the destination filename and sequence of proxies
#returns filename, list of all proxies/server
def readInput():
	if(len(sys.argv) <=1):
		raise Exception("Kindly pass the input file name in arguments or check readme.pdf")
	file = open(sys.argv[1], 'r')
	filename = file.readline()
	if(filename[len(filename)-1] == '\n'): #separating newline character from filename
		filename=filename[:-1]
	
	servers = [] #list that contains all proxies/server
	while True:
		line = file.readline()
		if(line == "\n"):
			continue
		if not line:
			break
		if(line[len(line)-1] == '\n'):
			line = line[:-1]
		servers.append(line)
	return filename, servers


#it connects client to the first proxy and saves the received data to the destination file
def sendAndRecvMessage(filename, host, port, req_sent):
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.settimeout(20)
	clientSocket.connect((host, port))
	clientSocket.settimeout(None)
	clientSocket.sendall(req_sent.encode()) #remaining proxies/servers list sent to the first proxy/server
	file_to_Download = open(filename, "w") #file to download
	while True:
		#receiving data bytes one by one
		clientSocket.settimeout(10)
		data = clientSocket.recv(1) #receiving data byte by byte
		clientSocket.settimeout(None)
		if not data:
			break
		file_to_Download.write(data.decode())
	clientSocket.close()


#starts from here
filename, servers = readInput()
if(len(servers) == 0):
	raise ValueError("server/proxy list is empty")
hp = servers[0]
hp = hp.split()
host = hp[0]
port = int(hp[1])
req_sent = createRequest(filename, servers)
sendAndRecvMessage(filename, host, port, req_sent)
print("received data successfully transferred to the file")