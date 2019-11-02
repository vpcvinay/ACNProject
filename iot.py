import time,socket,threading,sys
import random

def Iot_node(My_udp,N):
	print("Communicating to Fog_node")
	s_send=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	while True:
		message = raw_input("Enter Message:")
		MESSAGE = 'port:'+str(My_udp)+":"+str(message)
		ip="127.0.0.1"
		s_send.sendto(MESSAGE.encode(),random.choice(N))
		s_rsv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s_rsv.bind(("",My_udp))
		rsv_msg,addr = s_rsv.recvfrom(1024)
		print("Recieved Message : {}".format(rsv_msg.decode()))

if __name__=="__main__":
	My_udp = int(sys.argv[1])
	N = zip(sys.argv[2::2],map(int,sys.argv[3::2]))
	Iot_node(My_udp,N)
