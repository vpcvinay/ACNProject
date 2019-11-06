import time,socket,threading,sys
import random

def Iot_node(My_udp,N):
	print("Communicating to Fog_node")
	send_thread = threading.Thread(target=Send_comm,args=(My_udp,N,))
	recv_thread = threading.Thread(target=Recv_comm,args=(My_udp,N,))
	
	send_thread.start()
	recv_thread.start()
	
	send_thread.join()
	recv_thread.join()
	
	print("Communication Ended....")


def Send_comm(My_udp,N):
	s_send=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	while True:
		message = raw_input("Enter Message:")
		MESSAGE = 'port:'+str(My_udp)+":"+str(message)
		ip="127.0.0.1"
		s_send.sendto(MESSAGE.encode(),random.choice(N))
		if(message=="exit"):
			print("Ending the Send comm block")
			break

def Recv_comm(My_udp,N):	
	s_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s_rsv.bind(("",My_udp))
	while True:
		rsv_msg,addr = s_rsv.recvfrom(1024)
		if(rsv_msg.decode()=="exit"):
			print("Ending the Rev comm block")
			break
		print("Recieved Message : {}".format(rsv_msg.decode()))

if __name__=="__main__":
	My_udp = int(sys.argv[1])
	N = zip(sys.argv[2::2],map(int,sys.argv[3::2]))
	Iot_node(My_udp,N)
