import socket

MAX_DATA_VOLUME = 1024

sock = socket.socket()
sock.connect(("localhost", 6070))

try:
    while True:
        sock.send(str(input("Input package: ")).encode())
        data = sock.recv(MAX_DATA_VOLUME).decode()
        print(data)
except KeyboardInterrupt:
    pass
