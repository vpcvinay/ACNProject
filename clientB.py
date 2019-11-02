import time, socket,threading,sys
'''connection between fog nodes is done ,connection between iot to one fog node is done'''


#data,addr=iot_socket.recvfrom(1024)
#print("received message")
#print(data.decode())

class fog_node:
	def __init__(self,My_tcp,my_udp,C,Tcp0,N):
		self.received_conn = []
		self.iot_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.no_of_conn = 0
		self.N = N
		self.neighbors = len(N)
		self.My_tcp = My_tcp
		self.my_udp = my_udp
		self.cloud_ip = C
		self.cloud_port = Tcp0		
		self.My_ip = "127.0.0.1"
		self.iot_socket.bind(("",self.my_udp))
		
	def conn_establish(self):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		start = time.time()
		count = 0
		s.bind(("",self.My_tcp))
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
			for server in self.N:
				if server not in [port[1] for port in self.received_conn]:	
					s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					try:
						s.settimeout(2)
						s.connect(server)	
						print( "(", server, ")\n")
						time.sleep(1)
						print("Connected...\n")
						self.no_of_conn+=1
						self.received_conn.append((ip,server))
					except:
						continue
				
#fognode = fog_node()
#fognode.conn_establish()

if __name__=="__main__":
	My_tcp = int(sys.argv[1])
	My_udp = int(sys.argv[2])
	cloud_IP = sys.argv[3]
	cloud_port = int(sys.argv[4])
	N = zip(sys.argv[5::2],map(int,sys.argv[6::2]))
	Fog = fog_node(My_tcp,My_udp,cloud_IP,cloud_port,N)
	Fog.conn_establish()
	print(My_tcp,My_udp,cloud_IP,cloud_port,N)
		 
