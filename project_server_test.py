import time, socket, threading, sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip = "127.0.0.1"
port=6000
port_other = 1234
s.bind(('127.0.0.1', port_other))
s.listen(1)
conn, addr = s.accept()
print( "(", ip, ")\n")
print("connection establised")

