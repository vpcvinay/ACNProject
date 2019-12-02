import time,socket,threading,sys
import random

class variables:
	def __init__(self,interval,My_udp,N):
		self.N = N
		self.My_udp 	= My_udp
		self.interval	= interval
		self.ipaddr 	= "127.0.0.1"
		self.max_msg	= 10
		self.s_send 	= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		

def Iot_node(self):
	print("Communicating to Fog_node..... ")
	send_thread = threading.Thread(target=Send_comm,args=(self,))
	recv_thread = threading.Thread(target=Recv_comm,args=(self,))
	
	send_thread.start()
	recv_thread.start()
	
	send_thread.join()
	recv_thread.join()
	
	print("Communication Ended....")

def request_num_gen(self):
	count = 0
	while count<self.max_msg:
		count+=1
		yield count

def ip_addr(self):
	hostname=socket.gethostname()
	self.ipaddr=socket.gethostbyname(hostname)
	
def Send_comm(self):
	req_num = request_num_gen(self)
	while True:
		try:
			Seq_No = str(req_num.__next__())
		except StopIteration:
			Seq_No = "exit"
			#pass
		Req_Frwd_Lmt=random.randint(2,5)
		Req_Prcs_Tym=4#random.randint(3,7)
		if(Seq_No=="exit"):
			self.s_send.close()
			break
		#print(self.ipaddr)
		MESSAGE = self.ipaddr+":"+str(self.My_udp)+":Request from the IOT:"+Seq_No+":"+str(Req_Frwd_Lmt)+":"+str(Req_Prcs_Tym)+":"+"0:"
		node = random.choice(self.N)
		self.s_send.sendto(MESSAGE.encode(),node)
		print("Sending to message to the FOG node {} for the sequence : {}".format(node[0],Seq_No))
		time.sleep(self.interval)

def Recv_comm(self):
	count=0
	self.s_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	self.s_rsv.bind(("",self.My_udp))
	while True:
		rsv_msg,addr = self.s_rsv.recvfrom(1024)
		rsv_msg_d = rsv_msg.decode().split(":")
		#if(rsv_msg_d[-1]=="exit"):
		#	print("Ending the Rev comm block")
		#	break
		count+=1
		cloud_ip = rsv_msg_d[2].split(';')
		#print("Rsv_MSG ",cloud_ip)#rsv_msg_d[2].split(';'),len(rsv_msg_d[2].split(';')))
		#print("Cloud IP ",cloud_ip[-1])#rsv_msg_d[2].split(';')[-1])
		if len(cloud_ip)==2:
			nodes = ', '.join(cloud_ip[0].split(',')[:-1])
			print("Request hopped through {}".format(str(nodes)))
			print("Message with sequence ID {} Served by the Cloud {}".format(rsv_msg_d[1], cloud_ip[1]))
		else:
			fog_hopping = cloud_ip[0].split(',')[:-1]
			served_fog = fog_hopping.pop()
			fog_hopping = ', '.join(fog_hopping)
			if fog_hopping:
				print("Request Hopped through {}".format(fog_hopping))
			print("Message with sequence ID {} Served by the FOG node {}".format(rsv_msg_d[1],served_fog))
		
		#print(rsv_msg_d)
		#print("Response ".format(rsv_msg))
		if(count==self.max_msg):
			self.s_rsv.close()
			break
			

if __name__=="__main__":
	interval=float(sys.argv[1])/1000
	My_udp = int(sys.argv[2])
	N = list(zip(sys.argv[3::2],map(int,sys.argv[4::2])))
	var = variables(interval,My_udp,N)
	#ip_addr(var)
	Iot_node(var)
