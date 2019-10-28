import time, socket,threading,sys


print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
start = time.time()

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
	
def send():
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

def receive():
        ip = "127.0.0.1"
        port = 1234
        s.bind((ip, port))
        print("(", ip, ")\n")
        name = input(str("Enter your name: "))
        s.listen(1)
        print("\nWaiting for incoming connections...\n")
        conn, addr = s.accept()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")



        while 1:

            message = conn.recv(1024)
            message = message.decode()
            print(name, ":" ,message)
            print("")
            message = input(str("Please enter your message: "))
            conn.send(message.encode())
            print("Sent")
            print("")


