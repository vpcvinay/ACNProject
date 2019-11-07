import time, socket,threading,sys
import random
'''connection between fog nodes is done ,connection between iot to one fog node is done'''


#iot_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#iot_socket.bind(("",6000))
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
		self.My_udp = my_udp
		self.cloud_ip = C
		self.cloud_port = Tcp0		
		self.My_ip = "127.0.0.1"
		self.recv_queue=[]
		self.conn_state={}
		
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
					#self.received_conn.append(addr)
					self.no_of_conn+=1
					self.conn_state.update({addr:conn})
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
				print("connected to all neighbors and cloud")
				break
			for server in self.N+[(self.cloud_ip,self.cloud_port)]:
				if server not in [port[1] for port in self.received_conn]:	
					srv_soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					try:
						srv_soc.settimeout(2)
						srv_soc.connect(server)	
						print( "(", server, ")\n")
						time.sleep(1)
						print("Connected...\n")
						self.no_of_conn+=1
						#self.received_conn.append((ip,server))
						self.conn_state.update({server:srv_soc})
					except:
						continue
		iot_recv_thread=threading.Thread(target=self.iot_Recv_comm)
		iot_send_thread=threading.Thread(target=self.iot_Send_comm)

		fog_recv_thread=threading.Thread(target=self.fog_Recv_comm)
		fog_send_thread=threading.Thread(target=self.fog_Send_comm)
		
		iot_recv_thread.start()
		iot_send_thread.start()
		fog_recv_thread.start()
		fog_send_thread.start()
		
		iot_recv_thread.join()
		iot_send_thread.join()
		fog_recv_thread.join()
		fog_send_thread.join()
		
		print(self.conn_state)


	def iot_Recv_comm(self):
		iot_socket_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		iot_socket_rsv.bind(("",self.My_udp))
		while True:
			time.sleep(1)
			data,addr = iot_socket_rsv.recvfrom(1024)
			print(data.decode(),type(data.decode()))
			mesage = str(data.decode().split(":")[-1])
			self.recv_queue.append(data.decode())
			if(mesage == "exit"):
				print("Exiting the receive comm block")
				break
			print("Message received from ip : {} is : {}".format(addr,data.decode()))
			self.port = int(data.decode().split(":")[1])
				

	def iot_Send_comm(self):
		iot_socket_send=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		while True:
			time.sleep(1)
			Message = input("Enter the message:")
			iot_socket_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			iot_socket_send.sendto(Message.encode(),("127.0.0.1",self.port))
			if(Message=="exit"):	
				print("Exiting the send communication Block")
				break

	def fog_Send_comm(self):
		while True:
			while self.recv_queue and self.conn_state:
				rand_fog=random.choice(self.conn_state)
				msg=self.recv.pop(0)
				rand_fog.sendall(msg)
				print("messge sent to neighbour fog node {}".format(msg))
				mesage = str(msg.split(":")[-1])
				if(mesage == "exit"):
					print("Exiting the receive comm block")
					break
				time.sleep(1)
			time.sleep(1)
		

	def fog_Recv_comm(self):
		while True:
			#if self.recv
			for nodes in self.conn_state:
				try:
					msg=self.conn_state.get(nodes).recv(1024)
					print(msg.decode()) 
					mesage = str(msg.split(":")[-1].decode())
					if(mesage == "exit"):
						print("Exiting the receive comm block")
						break
				except:
					continue
		
		
if __name__=="__main__":
	My_tcp = int(sys.argv[1])
	My_udp = int(sys.argv[2])
	cloud_IP = sys.argv[3]
	cloud_port = int(sys.argv[4])
	N = list(zip(sys.argv[5::2],map(int,sys.argv[6::2])))
	Fog = fog_node(My_tcp,My_udp,cloud_IP,cloud_port,N)
	Fog.conn_establish()
	#print(My_tcp,My_udp,cloud_IP,cloud_port,N)
		 
