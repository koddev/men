
#!/usr/bin/env python3

import socket
from commands import Command
import time
import guid
# serverIP = '192.168.140.38'
serverIP='62.244.197.146'
# serverIP = '192.168.116.20'
httpPort = '8080'
tcpPort = 5551
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((serverIP, tcpPort))
# command = Command(sock)

def recvall(sock, buffer_size=4096):
    buf = sock.recv(buffer_size)
    while buf:
        yield buf
        if len(buf) < buffer_size: break
        buf = sock.recv(buffer_size)




def connect():
    data=""
    try:
        print('connecting...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((serverIP,tcpPort))

            guid = GUID()

            msg = {
                "guid": guid.uuid,
                "image": sendImage
            }
            sendMsg = json.dumps(msg)
            self.sock.send(sendMsg.encode())
    
        

            

