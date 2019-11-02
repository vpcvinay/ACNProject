import time,socket,threading,sys

class cloud_node:
	def __init__(self,ip,port):
		self.ip=ip
		self.port=port
		self.soc= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.incoming_ip=[]

	def connection_est(self):
		self.soc.bind(("",self.port))
		while True:
			time.sleep(1)
			try:
				self.soc.listen(6)
				conn,addr=self.soc.accept()
				self.incoming_ip.append(addr)
				print("Connection established")
				print("address and the port: {}".format(addr))
	
			except:
				continue
	


if __name__=="__main__":
	My_ip=sys.argv[1]
	My_tcp=int(sys.argv[2])
	
	cloud=cloud_node(My_ip,My_tcp)
	cloud.connection_est()

