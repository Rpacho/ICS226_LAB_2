#!/usr/bin/python3

import socket
import sys
import rolando
import Stuffing

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

if len(sys.argv) != 2:
    print(sys.argv[0] + ' <message>')
    sys.exit()

# Initiating socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print('Client:', sock.getsockname())

# sending data the first argument
add_n = sys.argv[1] + '\n'
data = add_n.encode('utf-8')
sock.sendall(data)

# Function for writing a file
def writeFile():
    path = "downloadedFiles/"
    f = open(path + sys.argv[1], "wb")
    fileData = Stuffing.unStuffing(sock)
    if(fileData != False):
        f.write(fileData)
    f.close()


writeFile()

# reply = sock.recv(BUF_SIZE)

# print(reply)


sock.close()

