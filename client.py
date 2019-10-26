import time, socket,threading,sys



print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()

def send():
	ip = "127.0.0.1"
	port=6000


	port_other = 1234
	s.connect(('127.0.0.1', port_other))

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


