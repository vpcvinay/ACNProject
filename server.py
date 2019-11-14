import time, socket,threading,sys
import random
"""1. To be done- fog to fog message forwarding
   2. Queue State exchange between fog nodes
   3. Fog to cloud message forwarding
   4. cloud to iot response"""

class fog_node:
	def __init__(self,My_tcp,my_udp,C,Tcp0,N,Max_Res_Tym,t):
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
		self.Max_Res_Tym=Max_Res_Tym
		self.t=t
		self.Q_Tym=0
		self.Frwd_Q=[]
		
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
						self.conn_state.update({server:srv_soc})
					except:
						continue
		iot_recv_thread=threading.Thread(target=self.iot_Recv_comm)
		iot_send_thread=threading.Thread(target=self.iot_Send_comm)
		#fog_recv_thread=threading.Thread(target=self.fog_Recv_comm)
		#fog_send_thread=threading.Thread(target=self.fog_Send_comm)
		iot_recv_thread.start()
		iot_send_thread.start()
		#fog_recv_thread.start()
		#fog_send_thread.start()
		
		iot_recv_thread.join()
		iot_send_thread.join()
		#fog_recv_thread.join()
		#fog_send_thread.join()
		
		print(self.conn_state)

	def iot_Recv_comm(self):
		iot_socket_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		iot_socket_rsv.bind(("",self.My_udp))
		while True:
			time.sleep(1)
			data,addr = iot_socket_rsv.recvfrom(1024)
			mesage = data.decode().split(":")
			Process_Tym=int(mesage[-1])
			if(self.Q_Tym+Process_Tym<=self.Max_Res_Tym):
				self.recv_queue.append(data.decode())
				self.Q_Tym+=Process_Tym
			else:
				self.Frwd_Q.append(data)
				self.Q_Tym+=Process_Tym
				if(mesage == "exit"):
					print("Exiting the receive comm block")
					break
			print("Message received from ip : {} is : {}".format(addr,data.decode()))
				

	def iot_Send_comm(self):
		iot_socket_send=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		#time.sleep(4)
		while True:
			time.sleep(1)
			if self.recv_queue:
				#time.sleep(1)
				iot_socket_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				Req_Prs=self.Req_Process()
				Message_send= "Reply to the IOT with Message ID:"+Req_Prs[-1]
				iot_socket_send.sendto(Message_send.encode(),(Req_Prs[0],Req_Prs[1]))
				print("Sent Reply to the IOT for message ID:"+Req_Prs[-1])
				if(Req_Prs[-1]=="exit"):
					print("Exiting the send communication Block")
					break
				
			else:
				print("No Message to Reply")

	def fog_Send_comm(self):
		print(self.conn_state)
		while True:
			#while self.recv_queue and self.conn_state:
			rand_fog=random.choice(list(self.conn_state.values()))
			#msg=self.recv.pop(0)
			msg = input("Enter Message to send")
			rand_fog.sendall(msg.encode())
			print("messge sent to neighbour fog node {}".format(msg))
			mesage = str(msg.split(":")[-1])
			if(mesage == "exit"):
				print("Exiting the receive comm block")
				break
			time.sleep(1)

	def Req_Process(self):
        	message=self.recv_queue.pop(0).split(":")
	        Process_Tym=int(message[-1])
        	time.sleep(Process_Tym)
	        self.Q_Tym-=Process_Tym
        	return [message[0],int(message[1]),message[3]]

	def fog_Recv_comm(self):
		while True:
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
	Max_Res_Tym = int(sys.argv[1])
	t=int(sys.argv[2])
	My_tcp = int(sys.argv[3])
	My_udp = int(sys.argv[4])
	cloud_IP = sys.argv[5]
	cloud_port = int(sys.argv[6])
	N = list(zip(sys.argv[7::2],map(int,sys.argv[8::2])))
	Fog = fog_node(My_tcp,My_udp,cloud_IP,cloud_port,N,Max_Res_Tym,t)
	Fog.conn_establish()
		 
