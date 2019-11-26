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
		self.up_time = 15

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
				print("Connection established")
				print("address and the port: {}".format(addr))
				print("Received *****",self.incoming_ip)
	
			except:
				continue
			#time.sleep(1)
	
	def fog_Recv(self):
		while True:
			if((time.time()-self.node_up_time)>self.up_time):
				print("ending fog recv thread ")
				break
			
			print("For Receive Loop *******\n")
			time.sleep(1)
			self.lock.acquire()
			connections = self.incoming_ip
			self.lock.release()
			for nodes in connections:
				#print("IP ip ip ip ip ip ip ",connections)
				try:
					nodes.settimeout(0.5)
					mesage=nodes.recv(1024).decode().split(":")
					print("Read message ",mesage)
					n=6
					mesage=[mesage[i*n:(i+1)*n] for i in range((len(mesage)+n-1)//n)]
					for msg in mesage:
						if msg[0]=='':
							continue
						data = ':'.join(msg)
						self.lock.acquire()
						self.fog_recv_msg.append(data)
						self.lock.release()
						print("Received Message from Fog ",self.fog_recv_msg)
					time.sleep(0.6)
				except:
					time.sleep(0.2)
					continue
			

	def iot_Send(self):
		while True:	
			if((time.time()-self.node_up_time)>self.up_time):
				print("ending iot send thread ")
				break
			
			print("Printing iot_send ********")
			time.sleep(1)
			if(not self.fog_recv_msg):
				#print("fog read buffer in not state ",self.fog_recv_msg)
				time.sleep(0.5)
				continue
			self.lock.acquire()
			msg=self.fog_recv_msg.pop(0).split(":")
			self.lock.release()
			print("Serving the message ",msg)
			ip,port,Seq_No,Res_Tym=msg[0],int(msg[1]),msg[3],float(msg[5])
			time.sleep(Res_Tym)
			with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as iot_soc:
				Message = "Cloud to Iot "+str(Seq_No) 
				print("Sending message to IOT")
				iot_soc.sendto(Message.encode(),(ip,port))
			#time.sleep(0.3)
			print("Sent ========================================")


if __name__=="__main__":
	My_ip="127.0.0.1"
	My_tcp=int(sys.argv[1])	
	cloud=cloud_node(My_ip,My_tcp)
	cloud.cloud()

