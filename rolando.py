#!/usr/bin/python3

import socket


# Receive data from the parameter until new line is found then return data
def receiveBytes(sc):
    #initial buffsize
    buff_size = 16
    end = b'\n'
    data = b''
    while True:
        reply = sc.recv(buff_size)
        for i in reply:
            if i.to_bytes(1, 'big') == end:
                return data
            else:
                data = data + i.to_bytes(1, 'big')
                #if the buffer is not enough increase the size
                if len(data) > buff_size:
                    buff_size = buff_size + 16
    #return data.decode('utf-8')
    return data
