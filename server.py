import time, socket,threading,sys


print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)


class fog_node:
	def __init__(self):
		self.received_conn = []
		self.no_of_conn = 0
		self.server_port=[6000,6001] #server port
		self.neighbors = len(self.server_port)
	
	def conn_establish(self):
		ip = "127.0.0.1"
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		start = time.time()
		client_port = 1234 #own port
		count = 0
		s.bind((ip,client_port))
		while count<self.neighbors:
			try:
				s.settimeout(6)
				s.listen(3)
				conn, addr = s.accept()
				if conn:
					print("Connection established with client with port : {}".format(addr[1]))
					count+=1
					self.received_conn.append(addr)
					self.no_of_conn+=1
					continue
			except:
				print("Connection not established")
				#s.shutdown(1)
				count+=1
				s.close()
				continue
		print("Number of connection established : {}".format(self.no_of_conn))
		while True:
			if self.no_of_conn==self.neighbors:
				print("connected to all neighbors")
				break
			for server in self.server_port:
				if server not in [port[1] for port in self.received_conn]:	
					s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					try:
						s.settimeout(2)
						s.connect(('127.0.0.1', server))	
						print( "(", server, ")\n")
						time.sleep(1)
						print("Connected...\n")
						self.no_of_conn+=1
						self.received_conn.append((ip,server))
					except:
						continue
				
fognode = fog_node()
fognode.conn_establish()

