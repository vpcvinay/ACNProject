import time,socket,threading,sys
MESSAGE = 'hello'
ip="127.0.0.1"
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(MESSAGE.encode(),("127.0.0.1",1234))

