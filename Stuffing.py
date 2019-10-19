#!/usr/bin/python3
import socket
import struct

ESC_CHAR = 27                                       # Esc character in binary
ESC = ESC_CHAR.to_bytes(1, 'big')                   # turn it to bytes

# This function is for stuffing and returns the data
# with start of ESC S end of ESC E and if there
# is an ESC in the middle of the then add 1 ESC aswell
def stuff(s):
    new_buffer = ESC + b'S'
    for x in s:
        encoded_x = x.to_bytes(1, 'big')
        if encoded_x == ESC:
            new_buffer = new_buffer + ESC
        new_buffer = new_buffer + encoded_x
    new_buffer = new_buffer + ESC + b'E'
    return new_buffer

# This function is for unstuffing and returns the data without
# the character that we insert in stuff function
def unStuffing(sock):
    buff_size = 128
    add_buff_size = 16
    stage = 1
    new_buffer = b''
    print("debug1")
    while True:
        reply = sock.recv(buff_size)
        if (reply == b''):              # if data that receive is empty then return
            return False
        for x in reply:
            encoded_x = x.to_bytes(1, 'big')
            print(encoded_x)
            if stage == 1 and encoded_x != ESC:
                print('Error in header')
                return ''
            elif stage == 1 and encoded_x == ESC:
                stage = 2
                continue
            if stage == 2 and encoded_x != b'S':
                print('Error in header')
                return ''
            elif stage == 2 and encoded_x == b'S':
                stage = 3
                continue
            if stage == 3 and encoded_x != ESC:
                new_buffer = new_buffer + encoded_x
                if (len(reply) > buff_size):        # if the buffer is not enough
                    buff_size = buff_size + add_buff_size   # add more
                continue
            if stage == 3 and encoded_x == ESC:
                stage = 4
                continue
            if stage == 4 and encoded_x == ESC:
                new_buffer = new_buffer + ESC
                if (len(reply) > buff_size):
                    buff_size = buff_size + add_buff_size
                stage = 3
                continue
            if stage == 4 and encoded_x == b'E':
                return new_buffer
            print('Error in stuffing')
            return ''
