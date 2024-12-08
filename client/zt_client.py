import socket
import base64

def upload(filename):
    with open(file=filename, mode="rb") as file:
        content = file.read()

    content_base64 = base64.b64encode(content).decode("utf-8")

    sock = socket.socket()
    sock.connect(("localhost", 6070))
    sock.send(f"zt_UPLOAD {filename} {content_base64}".encode())

    data = sock.recv(1024).decode()
    sock.close()

    print(data)

def download(filename):
    sock = socket.socket()
    sock.connect(("localhost", 6070))
    sock.send(f"zt_DOWNLOAD {filename}".encode())

    data = sock.recv(1024).decode()
    sock.close()

    content = base64.b64decode(data)

    with open(file=f"{filename}", mode="wb") as file:
        file.write(content)

def list_():
    sock = socket.socket()
    sock.connect(("localhost", 6070))
    sock.send("zt_LIST".encode())

    data = sock.recv(1024).decode()
    sock.close()

    print(data)

command = int(input("1: upload\n2: download\n3: list\n>>> "))

if command == 1:
    upload(filename=input("filename: "))

if command == 2:
    download(filename=input("filename: "))

if command == 3:
    list_()

input("enter to exit...")
