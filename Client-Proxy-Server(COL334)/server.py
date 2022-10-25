import sys
import socket
import threading

#It creates a message that is meant to be sent to the next proxy/server
def createRequestMsg(filename, servers):
	req_sent = filename+"\n"
	for i in range(1, len(servers)):
		req_sent += servers[i]+'\n'
	return req_sent

#whenever a new client hand-shakes with the server
def new_client(clientsocket,addr, Id):
	data_recv = clientsocket.recv(4096)
	data_recv = data_recv.decode()
	data = data_recv.split("\n")
	while(data[len(data)-1] == None or data[len(data)-1] == "\n" or data[len(data)-1] == ""): #removing unnecessary entries
		data = data[:-1]
	if(len(data) < 1):
		return;
	if(len(data) == 1): #it is a server
		print(f"Working as a server in thread {Id}")
		file = open(data[0], 'r') #0th element of data is desired file's name
		while True:
			char = file.read(1) #reading file byte by byte
			if not char:
				break
			clientsocket.send(char.encode()) #sending byte by byte continuously
	else: #it is a proxy
		print(f"Working as a proxy in thread {Id}")
		filename = data[0]
		servers = []
		for i in range(1, len(data)):
			servers.append(data[i])
		hp = servers[0].split( )
		host = hp[0]
		port = int(hp[1])
		#create a client socket to connect with next proxy/server
		newcSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		newcSocket.settimeout(20)
		newcSocket.connect((host, port))
		newcSocket.settimeout(None)
		
		req_sent = createRequestMsg(filename, servers)
		newcSocket.sendall(req_sent.encode())
		
		while True:
			newcSocket.settimeout(10)
			data = newcSocket.recv(1) #receiving data byte by byte
			newcSocket.settimeout(None)
			if not data:
				break
			clientsocket.send(data) #sending data continuously
		newcSocket.close()
	print(f"file sending in thread {Id} completed")
	clientsocket.close()


class myThread (threading.Thread):
	def __init__(self, c, addr, Id):
		threading.Thread.__init__(self)
		self.Id = Id
		self.c = c
		self.addr = addr
	def run(self):
		new_client(self.c, self.addr, self.Id)

#starts from here
port = -1
if(len(sys.argv) > 1):
	port = int(sys.argv[1])
else:
	print("Enter the port no. : ")
	port = int(input())


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(5) #max 5 connections can be kept in waiting
print("the server is ready")
count = 0
while True:
	c, addr = serverSocket.accept()
	print(f"creating new thread {count}")
	thread = myThread(c, addr, count)
	thread.start()
	count+=1

s.close()