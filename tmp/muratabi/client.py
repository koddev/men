#!/usr/bin/env python3

import socket
from commands import Command

#serverIP = '192.168.140.38'
serverIP = '192.168.116.20'
httpPort = '8080'
tcpPort = 5551
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((serverIP, tcpPort))
command = Command(sock)

def recvall(sock, buffer_size=4096):
    buf = sock.recv(buffer_size)
    while buf:
        yield buf
        if len(buf) < buffer_size: break
        buf = sock.recv(buffer_size)

command.faceCapture.startImageStream(command.settings.settings["resolution"], command.settings.settings["fps"])
data = ''
while True:
    #data = sock.recv(1024).decode()
    data += b''.join(recvall(sock)).decode('UTF-8')
    if data[-1] == "\n":
        command.parse_command(data)
        data = ''
sock.close()
