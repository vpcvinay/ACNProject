import time,socket,threading,sys
import random

class variables:
	def __init__(self,interval,My_udp,N):
		self.N = N
		self.My_udp = My_udp
		self.interval=interval


def Iot_node(self):
	print("Communicating to Fog_node")
	send_thread = threading.Thread(target=Send_comm,args=(self,))
	recv_thread = threading.Thread(target=Recv_comm,args=(self,))
	
	send_thread.start()
	recv_thread.start()
	
	send_thread.join()
	recv_thread.join()
	
	print("Communication Ended....")

def request_num_gen():
	count = 0
	while count<10:	
		count+=1
		yield count
def ip_addr(self):
	hostname=socket.gethostname()
	self.ipaddr=socket.gethostbyname(hostname)
	
def Send_comm(self):
	s_send=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	req_num = request_num_gen()
	ip_addr(self)
	while True:
		try:
			Seq_No = str(req_num.__next__())
		except StopIteration:
			Seq_No = "exit"
		Req_Frwd_Lmt=2#random.randint(2,5)
		Req_Prcs_Tym=3#random.randint(3,7)
		MESSAGE = self.ipaddr+":"+str(self.My_udp)+":Request from the IOT:"+Seq_No+":"+str(Req_Frwd_Lmt)+":"+str(Req_Prcs_Tym)+":"
		s_send.sendto(MESSAGE.encode(),random.choice(self.N))
		print("Sent message to FOG with ID:"+Seq_No)
		if(Seq_No=="exit"):
			print("Ending the Send comm block")
			break
		time.sleep(self.interval)

def Recv_comm(self):
	s_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s_rsv.bind(("",self.My_udp))
	while True:
		rsv_msg,addr = s_rsv.recvfrom(1024)
		rsv_msg_d = rsv_msg.decode().split(":")
		if(rsv_msg_d[-1]=="exit"):
			print("Ending the Rev comm block")
			break
		print("Recieved Message : {}".format(rsv_msg))

if __name__=="__main__":
	interval=float(sys.argv[1])/1000
	My_udp = int(sys.argv[2])
	N = list(zip(sys.argv[3::2],map(int,sys.argv[4::2])))
	var = variables(interval,My_udp,N)
	Iot_node(var)
