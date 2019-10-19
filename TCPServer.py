#!/usr/bin/python3

import socket
import rolando # For getting the files until \n is found
import Stuffing
import struct

BUF_SIZE = 1024
HOST = ''
PORT = 12345
FOLDERFILE = "server/"  # The server folder

# This is for setting up connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
print('Server: ' ,sock.getsockname())

# This function take the file name as parameter and find it in directory
# and it read the file data as binary code and return it
def getFile(file):
    fileName = FOLDERFILE + file.decode('utf-8')
    try:
        f = open(fileName, "rb")
        readFile = f.read()
        #print(readFile)
        f.close()
        return readFile
    except Exception:
        print("File not Found")

# This is when we accept a connection
# read the argument then find that file and
while True:
    sc, sockname = sock.accept()
    print('Client:', sc.getpeername())
    fileName = rolando.receiveBytes(sc) # The receiveBytes returns the data we received until the '\n'
    print(fileName)
    data = getFile(fileName)
    # if the given file name is valid then send the
    # data to client by buffer size until the length of the data is 0
    if(data):
        lengthData = len(data)
        j = 0
        buffer_size = BUF_SIZE
        while True: 
            binary_data = b''
            i = 0
            if lengthData < BUF_SIZE:
                buffer_size = lengthData
            while i < buffer_size:
                binary_data = binary_data + data[j].to_bytes(1, 'big')
                i = i + 1
                j = j + 1
            lengthData = lengthData - BUF_SIZE
            sc.sendall(binary_data)
            if lengthData < 0:
                break
        

    sc.close()


