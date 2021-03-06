import time, socket,threading,sys
import random
"""1. To be done- best fog node chooice
   2. not to forward to the node from which it received the request
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
		self.cloud_Q=[]
		self.Q_state={}
		self.lock=threading.Lock()
		self.cloud_node=[]
		self.node_up_time = time.time()
		self.up_time = 100

	def getIP(self):
		hostname = socket.gethostname()
		self.My_ip = socket.gethostbyname(hostname)

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
					print("Connection established with Neighbor FOG IP : {} and  port : {}".format(addr[0],addr[1]))
					count+=1
					#self.received_conn.append(addr)
					self.no_of_conn+=1
					self.conn_state.update({addr:conn})
					continue
			except:
				#print("Connection not established")
				#s.shutdown(1)
				count+=1
				s.close()
				continue
		#print("Number of connection established : {}".format(self.no_of_conn))
		
		while True:
			if self.no_of_conn==self.neighbors+1:
				print("connected to all Neighbor nodes and Cloud node")
				break
			for server in self.N+[(self.cloud_ip,self.cloud_port)]:
				if server not in self.conn_state.keys():
					if server in [(self.cloud_ip,self.cloud_port)] and self.cloud_node:
						time.sleep(1)
						continue
					
					srv_soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					try:
						srv_soc.settimeout(2)
						srv_soc.connect(server)
						time.sleep(1)
						self.no_of_conn+=1
						if server in [(self.cloud_ip,self.cloud_port)]:
							print("Connection Established with Cloud : {}".format(server))
							self.cloud_node.append(srv_soc)
							continue
						print("Connection Established with Neighbor FOG IP : {} and port : {}".format(server[0],server[1]))
						self.conn_state.update({server:srv_soc})
					except:
						continue
		
		print("\n")
		iot_recv_thread=threading.Thread(target=self.iot_Recv_comm)
		iot_send_thread=threading.Thread(target=self.iot_Send_comm)
		fog_recv_thread=threading.Thread(target=self.fog_Recv_comm)
		fog_send_thread=threading.Thread(target=self.fog_Send_comm)
		fog_cloud_thread=threading.Thread(target=self.fog_cloud_msg)

		iot_recv_thread.start()
		iot_send_thread.start()
		fog_recv_thread.start()
		fog_send_thread.start()
		fog_cloud_thread.start()
		time.sleep(2)
		
		iot_recv_thread.join()
		iot_send_thread.join()
		fog_recv_thread.join()
		fog_send_thread.join()
		fog_cloud_thread.join()
			

	def fog_cloud_msg(self):
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("Ending fog cloud end ")
				break
			
			#print("Cloud node buffer *****",self.cloud_Q)
			if not self.cloud_Q:
				time.sleep(1)
				continue
			msg=self.cloud_Q.pop(0)
			seq_no = msg.split(":")[3]
			print("Forwarding packet with seq_no {} to Cloud".format(seq_no))
			self.cloud_node[0].sendall(msg.encode())
			time.sleep(1)
		
	def iot_Recv_comm(self):
		iot_socket_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		iot_socket_rsv.bind(("",self.My_udp))
		#ip_addr:UDP:message:Seq_No:Forward_Limit:Processing_Time:0:
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("Iot recv comm end ")
				iot_socket_rsv.close()
				break
			
			time.sleep(1)
			try:
				iot_socket_rsv.settimeout(0.5)
				data,addr = iot_socket_rsv.recvfrom(1024)
				n=7
				print("Request Received {} from IOT {}".format(data.decode(),addr[0]))
				mesage = data.decode().split(":")
				mesage=[mesage[i*n:(i+1)*n] for i in range((len(mesage)+n-1)//n)]
				for msg in mesage:
					if msg[0]=='':
						continue
					Process_Tym=int(msg[5])
					if(self.Q_Tym+Process_Tym<=self.Max_Res_Tym):
						self.lock.acquire()
						data = ':'.join(msg)
						#print("Adding iot received msg for processing ######## : {}".format(data))
						self.recv_queue.append(data)
						self.lock.release()
						self.Q_Tym+=Process_Tym
					else:
						msg[4]=str(int(msg[4])-1)
						#msg[6] = str(self.My_udp)+','
						data = ':'.join(msg+[''])
						if(int(msg[4])==0):
							self.cloud_Q.append(data)
							#print("Sending data to cloud buffer $$$$$$$$$ : {}".format(data))
							continue
						#print("Sending data to Fog send buffer &&&&&&& : {}".format(data))
						self.Frwd_Q.append((data,addr))
						if(msg[4] == "exit"):
							#print("Exiting the receive comm block")
							break
					#print("Message received from iot : {} is : {}".format(addr,data))
			except:
				continue

	def iot_Send_comm(self):
		iot_socket_send=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		#time.sleep(4)
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("Iot send comm end ")
				iot_socket_send.close()
				break
			time.sleep(1)
			if self.recv_queue:
				#time.sleep(1)
				#iot_socket_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				Req_Prs=self.Req_Process()
				hopped_nodes = Req_Prs[3].split(',')
				Req_Prs[3] = ','.join(hopped_nodes[:-1]+[str(self.My_ip)]+[''])
				Message_send= ':'.join(["Reply to the IOT with Message ID ",Req_Prs[2],Req_Prs[3]])
				iot_socket_send.sendto(Message_send.encode(),(Req_Prs[0],Req_Prs[1]))
				print("Sent Reply to the IOT {} for message ID : {}".format(Req_Prs[0],Req_Prs[2]))
				if(Req_Prs[-1]=="exit"):
					print("Exiting the send communication Block")
					break
				
			#else:
				#print("No Message to Reply")

	def fog_Send_comm(self):
		start_time=time.time()
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("Fog Send node end ")
				break
			crnt_time=time.time()
			while self.Frwd_Q and self.conn_state:
				msg=self.Frwd_Q.pop(0)
				mesg = msg[0].split(":")
				hopped_nodes = mesg[6].split(',')
				mesg[6] = ','.join(hopped_nodes[:-1]+[str(self.My_ip),''])
				#print("Fog send Q mesg's : {} \n".format(mesg))
				msg = ':'.join(mesg)
				#print("Fog senf Q msg : {} \n".format(msg))
				
				if(int(mesg[4])==0):
					#print("Sending the message to Cloud buffer at FOG send ",msg)
					self.cloud_Q.append(msg)
					#print("appending to cloud_Q ",self.cloud_Q)
					continue
				fog_node = self.best_Fog_node_selection(msg[1],hopped_nodes)
				#print("Printing the output ===== {}\n".format(fog_node))
				if fog_node:
					#print("Forwarding message to Fog : {}".format(msg,fog_node))
					#print("Conn State is ===== {}\n".format(self.conn_state.get((fog_node[0],int(fog_node[1])))))
					self.conn_state.get(fog_node).sendall(msg.encode())
					print("Forwarding the message : {} to best node {}".format(msg,fog_node[0]))
				else:
					#print("No Best Fog node to forward data, sending to cloud ****** ")
					self.cloud_Q.append(msg)

				#mesage = str(msg.split(":")[4])
				#if(mesage == "exit"):
				#	print("Exiting the receive comm block")
				#	break
				time.sleep(1)
			
			if(not self.conn_state and self.Frwd_Q):
				msg = self.Frwd_Q.pop(0)
				self.cloud_Q.append(msg[0])
				#print("No available Fog node ",self.cloud_Q)
				
			if(crnt_time-start_time>=3.0):
				self.Forward_Qstate()
				start_time=crnt_time


	def Forward_Qstate(self):
		Qstate_msg="Q:"+self.My_ip+":"+str(self.My_tcp)+":"+str(self.Max_Res_Tym)+":"+str(self.Q_Tym)+":0:"
		#print("Qstate is : {}".format(Qstate_msg))
		for ip in self.conn_state:
			desc = self.conn_state.get(ip)
			print("Forwarding Q_state to IP : {}".format(ip[0]))
			desc.sendall(Qstate_msg.encode())
			
	def best_Fog_node_selection(self,node,hopped_nodes):
		best_capacity = 0
		best_node = 0
		ports = [str(port[1]) for port in self.N]
		for qstate in self.Q_state:
			if(qstate==node):
				continue
			if(qstate[0] in hopped_nodes):
				continue
			max_res_Tym,q_Tym = self.Q_state.get(qstate)
			capacity = float(max_res_Tym)-float(q_Tym)
			if capacity>best_capacity:
				best_capacity = capacity
				best_node = qstate
		#print("Printing the best_node : {}".format(best_node))
		return best_node

	def Req_Process(self):
		self.lock.acquire()
		message=self.recv_queue.pop(0).split(":")
		print("Processing the Request : {}".format(message[3]))
		self.lock.release()
		Process_Tym=int(message[5])
		time.sleep(Process_Tym)
		nodes_hopped = message[6]
		self.Q_Tym-=Process_Tym
		return [message[0],int(message[1]),message[3],nodes_hopped]

	def fog_Recv_comm(self):
		#self.QQqueue = []
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("Fog Recv end ")
				break
			for nodes in self.conn_state:
				time.sleep(1)
				try:
					self.conn_state.get(nodes).settimeout(0.5)
					data=self.conn_state.get(nodes).recv(1024)
					n=7
					mesage = data.decode().split(":")
					mesage=[mesage[i*n:(i+1)*n] for i in range((len(mesage)+n-1)//n)]
					for msg in mesage:
						if msg[0]=='':
							continue
						#print("Message : {} received from : {}".format(data,nodes))
						if(msg[0]=="Q"):
							#decode_msg=msg.decode().split(":")
							print("Q_State received from FOG node : {}".format(nodes[0]))
							self.Q_state.update({nodes:tuple(msg[3:5])})
							#print("The Q_state is :{}".format(self.Q_state))
							continue
						else:
							print("Received the IOT request : {} from FOG node : {}".format(data,nodes[0]))
							#print("entering else")
							#mesage = str(msg.split(":")[3].decode())
							msg[4] = str(int(msg[4])-1)
							data = ':'.join(msg+[''])
							#print("Extracted message at FOG recv buffer ",data)
							if(self.Q_Tym+int(msg[5])>self.Max_Res_Tym):
								self.Frwd_Q.append((data,nodes))
								#print("Fog buffer full, sending to next FOG HOP ",data,nodes)
								continue
							else:
								self.Q_Tym+=int(msg[5])
								self.recv_queue.append(data)
								#print("Sending to processing buffer ",data)
							if(mesage == "exit"):
								#print("Exiting the receive comm block")
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
	Fog.getIP()
	Fog.conn_establish()
	
