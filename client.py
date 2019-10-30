import time, socket,threading,sys


print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
start = time.time()

def fog_node_connect():
	ip = "127.0.0.1"
	client_port = 1234 #own port
	server_port=6000 #server port
	conn_establ = False
	while True:
		try:
			s.bind((ip,client_port))
			try:
				s.settimeout(2)
				s.listen(1)
				conn, addr = s.accept()
				if conn:
					print("Connection established with client with port : {}".format(client_port))
					conn_establ = True
					break
			except:
				print("Connection not established")
				s.shutdown(1)
				s.close()
				break
		except:
			print("Unable to connect")
			break
	
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('127.0.0.1', server_port))

	print( "(", ip, ")\n")
	name = input(str("\nEnter your name: "))

	print("\nTrying to connect to ", "(", port_other, ")\n")
	time.sleep(1)

	print("Connected...\n")

	while 1:
		message = input(str("Please enter your message: "))
		message = message.encode()
		s.send(message)
		print("Sent")
		print("")
		message = s.recv(1024)
		message = message.decode()
		print(name, ":" ,message)
		print("")

if not conn_establ:
	send()
