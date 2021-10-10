#!/usr/bin/env python3

from json.decoder import JSONDecodeError
import sys
import os
import socket
import json
import select
import time
from HashTable import HashTable

# Constants
HEADER_SIZE = 64
COMP_SIZE   = 100
ENCODING    = 'utf-8'
DISCONNECT  = 'DC'
BAD_REQUEST = {'status': 'Bad Request'}

#Sends length padded to HEADER_SIZE Bytes then data
def sendData(conn, msg):
    message = msg.encode(ENCODING)
    sendLen = str(len(message)).encode(ENCODING)
    sendLen += b' '*(HEADER_SIZE-len(sendLen))
    message = sendLen + message
    conn.sendall(message)

#Handles the request once it has been transformed into a JSON object
def handleRequest(conn, req, ht):
    if req["method"] == "insert":
        logTransaction(req, ht)
        ht.insert(req["key"], req["value"])
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    elif req["method"] == "lookup":
        val = ht.lookup(req["key"])
        req["value"] = val
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    elif req["method"] == "remove":
        logTransaction(req, ht)
        val = ht.remove(req["key"])
        req["value"] = val
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    elif req["method"] == "scan":
        val = ht.scan(req["regex"])
        req["matches"] = val
        sendData(conn, json.dumps({"status": "OK", "data": req}))

    else:
        sendData(conn, json.dumps(BAD_REQUEST))

#When a socket has data to be read from, fulfill the reqquest
def handleClient(conn, ht):
    connected = True
    msgLen = conn.recv(HEADER_SIZE).decode(ENCODING)
    if msgLen == DISCONNECT: connected = False

    if msgLen and msgLen != DISCONNECT:
        try:
            msgLen = int(msgLen)
            lenRead = 0
            req = ''

            while lenRead < msgLen:
                resp = conn.recv(msgLen-lenRead).decode(ENCODING)
                lenRead += len(resp)
                req += resp

            if req == DISCONNECT: connected = False
            req = json.loads(req)
            handleRequest(conn, req, ht)
        except:
            sendData(conn, json.dumps(BAD_REQUEST))
    
    if ht.txns >= COMP_SIZE: compactLog(ht)

    return connected
    

# Append a transaction to table.txn
# Format: 
# {"method": "insert", "key": x "value": y}
# {"method": "remove", "key": x}
def logTransaction(req, ht):
    ht.txn.write(json.dumps(req)+"\n")
    ht.txns += 1

# Replace table.ckpt with data in ht and delete transactions
def compactLog(ht):
    ckpt = open("tmp.ckpt", "w+")
    ckpt.write(json.dumps(ht.d))
    ckpt.flush()
    os.fsync(ckpt)
    ckpt.close()
    try:
        os.remove("table.ckpt")
        ht.txn.close()
        os.remove("table.txn")
        ht.txns = 0
        ht.txn = open("table.txn", "a")
    except:
        print("Unable to remove tmp.ckpt or wipe table.txn")

    os.rename("tmp.ckpt", "table.ckpt")

# Load existing data
def loadData(ht):
    # Open ckpt file and read data into ht
    try: 
        ckpt = open("table.ckpt", "r")
        ht.d = json.loads(ckpt.read())
        ckpt.close()
    except OSError:
        print("No pre-existing data in ckpt")
    except JSONDecodeError:
        print("Unable to read existing data, something went quite wrong")
    # Open transaction file and do all transactions
    try:
        txn = open("table.txn", "r")
        for line in txn:
            ht.txns += 1
            req = json.loads(line)
            if req["method"] == "insert":
                ht.insert(req["key"], req["value"])
            elif req["method"] == "remove":
                ht.remove(req["key"])
        txn.close()
    except OSError:
        print("No pre-existing transactions")
    except JSONDecodeError:
        print("Unable to read existing logging, something is very wrong")

    ht.txn = open("table.txn", "a")

def main():
    
    # Check input args
    if len(sys.argv) != 2:
        print("Usage: python3 HashTableServer.py PORTNUM")
        print("PORTNUM of 0 will choose first available port")
        return

    PORT   = int(sys.argv[1])
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR   = (SERVER, PORT)
    ht     = HashTable()

    print('Loading Data...')
    loadData(ht)

    print('Starting server...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.bind(ADDR)
    sock.listen(5)
    print(f'Listening on {SERVER}:{sock.getsockname()[1]}...')

    connections = [ sock ]
    readable = []

    # Amount of requests to skip for logging (Too many to see)
    logVal = 500
    reqs = 0

    print('Accepting clients...')
    while True:
        try:
            # writable and exceptions are not needed since we dont have to wait for a socket to be readable we jsut send the response
            readable, writable, exceptions = select.select(connections, connections, connections)

            for conn in readable: 
                if conn == sock:
                    new_conn, addr = conn.accept()
                    new_conn.setblocking(0)
                    print(f'[{new_conn.getpeername()[0]}] Connected')
                    connections.append(new_conn)
                else:
                    reqs += 1
                    if reqs == logVal: 
                        print(f'[{conn.getpeername()[0]}] Handling request')
                        reqs = 0
                    
                    connected = handleClient(conn, ht)
                    if not connected:
                        connections.remove(conn)
                        print(f'[{conn.getpeername()[0]}] Connection closed gracefully')
                        conn.close()

            for conn in exceptions:
                connections.remove(conn)
                print(f'[{conn.getpeername()[0]}] Connection crashed')
                conn.close()

        except KeyboardInterrupt:
            print('\nStopping server...')
            for conn in connections:
                if conn != sock:
                    sendData(conn, DISCONNECT)
                    conn.close()
            sock.close()
            print("Goodbye!")
            break
        

if __name__ == "__main__":
    main()