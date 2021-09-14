#!/usr/bin/env python3

import sys
import socket
from HashTable import HashTable

def handleConnection(conn):
    while True:
        header = conn.recv(1024)
        if not header:
            break
        print(header)

def main():
    
    #Check input args
    if len(sys.argv) != 2:
        print("Usage: python3 HashTableServer.py PORTNUM")
        print("PORTNUM of 0 will choose first available port")
        return

    portNum = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', portNum))
    
    while True:
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print('Connected to by: ', addr)
            handleConnection(conn)

if __name__ == "__main__":
    main()