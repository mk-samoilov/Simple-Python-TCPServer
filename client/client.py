import socket

sock = socket.socket()
sock.connect(("localhost", 6070))
sock.send(str(input("Input message: ")).encode())

data = sock.recv(1024).decode()
sock.close()

print(data)
