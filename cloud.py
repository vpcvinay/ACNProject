import time,socket,threading,sys
from threading import Lock

class cloud_node:
	def __init__(self,ip,port):
		self.ip=ip
		self.port=port
		self.soc= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.incoming_ip=[]
		self.fog_recv_msg=[]
		self.lock = Lock()
		self.node_up_time = time.time()
		self.up_time = 120
	
	def getIP(self):
		hostname = socket.gethostname()
		self.ip = socket.gethostbyname(hostname)

	def cloud(self):
		cloud_fog_Conn_thread=threading.Thread(target=self.connection_est)
		cloud_iot_send_thread=threading.Thread(target=self.iot_Send)
		cloud_fog_recv_thread=threading.Thread(target=self.fog_Recv)

		cloud_fog_Conn_thread.start()
		cloud_iot_send_thread.start()
		cloud_fog_recv_thread.start()

		cloud_fog_Conn_thread.join()
		cloud_iot_send_thread.join()
		cloud_fog_recv_thread.join()
		
		
	def connection_est(self):
		self.soc.bind(("",self.port))
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("ending connection thread ")
				break
			
			time.sleep(1)
			try:
				self.soc.listen(6)
				self.soc.settimeout(0.5)
				conn,addr=self.soc.accept()
				self.lock.acquire()
				self.incoming_ip.append(conn)
				self.lock.release()
				print("Incoming Request from the FOG {} accepted and connected....".format(addr[0]))
				#print("address and the port: {}".format(addr))
				#print("Received *****",self.incoming_ip)
	
			except:
				continue
			#time.sleep(1)
	
	def fog_Recv(self):
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("Fog Receive Thread Ended ")
				break
			
			#print("Fog Receive Loop ------- \n")
			time.sleep(1)
			self.lock.acquire()
			connections = self.incoming_ip
			self.lock.release()
			for nodes in connections:
				#print("IP ip ip ip ip ip ip ",connections)
				try:
					#print(nodes)
					nodes.settimeout(0.5)
					mesage = nodes.recv(1024)
					#print("Received MSG",mesage)
					#print("decoded",mesage.decode().split(":"))
					mesage = mesage.decode().split(":")
					#print(mesage)
					srv_fog = mesage[6].split(',')[-2]
					print("IOT Message with Sequence ID {} Received from FOG : {}".format(mesage[3],srv_fog))
					n=7
					mesage=[mesage[i*n:(i+1)*n] for i in range((len(mesage)+n-1)//n)]
					for msg in mesage:
						if msg[0]=='':
							continue
						data = ':'.join(msg)
						self.lock.acquire()
						self.fog_recv_msg.append(data)
						self.lock.release()
						#print("Sent the Received message : {} >>>>>> for processing".format(data))
					time.sleep(0.6)
				except:
					time.sleep(0.2)
					continue
	

	def iot_Send(self):
		while True:	
			if((time.time()-self.node_up_time)>self.up_time):
				print("ending iot send thread ")
				break
			#print("Iot send block \n")	
			time.sleep(1)
			if(not self.fog_recv_msg):
				#print("fog read buffer in not state ",self.fog_recv_msg)
				time.sleep(0.5)
				continue
			self.lock.acquire()
			msg=self.fog_recv_msg.pop(0).split(":")
			self.lock.release()
			print("Serving the IOT Message with ID : {}..... ".format(msg[3]))
			ip,port,Seq_No,Res_Tym = msg[0],int(msg[1]),msg[3],float(msg[5])
			hopped_nodes = msg[6].split(',')
			msg[6] = ','.join(hopped_nodes[:-1]+[';'+self.ip])
			#print("printing the message ",msg[6])
			time.sleep(Res_Tym)
			with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as iot_soc:
				Message = ':'.join(["Cloud to Iot ",str(Seq_No),msg[6]])
				print("Response Sent to IOT for packet : {}".format(Seq_No))
				iot_soc.sendto(Message.encode(),(ip,port))
			#time.sleep(0.3)
			#print("Sent ========================================")


if __name__=="__main__":
	My_ip="127.0.0.1"
	My_tcp=int(sys.argv[1])
	cloud=cloud_node(My_ip,My_tcp)
	#cloud.getIP()
	cloud.cloud()

