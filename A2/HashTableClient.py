import socket
import json

class HashTableClient():

    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def sendJson(self, jsonObj):
        self.sock.sendall(bytearray(json.dumps(jsonObj)))

    def recieveJson(self):
        return json.loads(self.sock.recv(1024))

    def close(self):
        self.sock.close()
