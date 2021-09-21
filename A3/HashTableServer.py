#!/usr/bin/env python3

import sys
import socket
import json
import time
from HashTable import HashTable

# Constants
HEADER_SIZE = 64
ENCODING    = 'utf-8'
DISCONNECT  = 'DC'
BAD_REQUEST = {'status': 'Bad Request'}

def sendHeader(conn, msgLen):
    sendLen = str(msgLen).encode(ENCODING)
    #Add padding to make lenght of header correct
    sendLen += b' '*(HEADER_SIZE-len(sendLen))
    conn.send(sendLen)

def sendData(conn, msg):
    message = msg.encode(ENCODING)
    print(len(message))
    sendHeader(conn, len(message))
    time.sleep(1)
    conn.send(message)

def handleRequest(conn, req, ht):
    #print(f'[REQUESTED] {req}')
    if req["method"] == "insert":
        ht.insert(req["key"], req["value"])
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    elif req["method"] == "lookup":
        val = ht.lookup(req["key"])
        req["value"] = val
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    elif req["method"] == "remove":
        val = ht.remove(req["key"])
        req["value"] = val
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    elif req["method"] == "scan":
        val = ht.scan(req["regex"])
        req["matches"] = val
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    else:
        sendData(conn, json.dumps(BAD_REQUEST))

def handleClient(conn, addr, ht):
    print('Connected to by: ', addr)

    connected = True
    while connected:
        msgLen = conn.recv(HEADER_SIZE).decode(ENCODING)
        if msgLen == DISCONNECT:
            print("Closing connection...")
            connected = False
        # Can only be converted to int if it exists
        if msgLen and msgLen != DISCONNECT: 
            msgLen = int(msgLen)
            req = conn.recv(msgLen).decode(ENCODING)
            if req == DISCONNECT: connected = False
            try:
                req = json.loads(req)
                handleRequest(conn, req, ht)
            except:
                sendData(conn, json.dumps(BAD_REQUEST))

    conn.close()


def main():
    
    #Check input args
    if len(sys.argv) != 2:
        print("Usage: python3 HashTableServer.py PORTNUM")
        print("PORTNUM of 0 will choose first available port")
        return

    PORT   = int(sys.argv[1])
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR   = (SERVER, PORT)
    ht     = HashTable()

    print('Starting server...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.bind(ADDR)
    sock.listen()
    print(f'Listening on {SERVER}:{sock.getsockname()[1]}...')
    print('Accepting clients...')
    
    while True:
        sock.settimeout(1.0)
        try:
            conn, addr = sock.accept()
            handleClient(conn, addr, ht)
        except socket.timeout:
            try:
                pass
            except KeyboardInterrupt:
                print('Stopping server...')
                sock.close()
                print("Goodbye!")
        

if __name__ == "__main__":
    main()