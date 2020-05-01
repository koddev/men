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

while True:
    data = sock.recv(1024).decode()
    command.parse_command(data)

sock.close()
