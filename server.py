import time, socket, sys

print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
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


receive()
