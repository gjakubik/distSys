from json.decoder import JSONDecodeError
import socket
import json
import http

# Constants
HEADER_SIZE = 64
ENCODING    = 'utf-8'
DISCONNECT  = 'DC'
CATALOG     = ('catalog.cse.nd.edu', 9097)

class HashTableClient():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
    def connSock(self, projName):
        print(f"Finding {projName} on {CATALOG[0]}:{CATALOG[1]}")

        try:
            conn = http.client.HTTPConnection(CATALOG)

            conn.request('GET', '/query.json')

            resp = conn.getresponse()

            respJSON = json.loads(resp.read().decode(ENCODING))

            print(respJSON)

            serverCandidates = filter(lambda x: x['project'] == projName and x['type'] == 'hashtable', respJSON)
            
            print(serverCandidates)
            
            recent = 0
            for candidate in serverCandidates:
                if candidate['lastheardfrom'] > recent:
                    recent = candidate['lastheardfrom']
                    serverObj = candidate
                
            host = serverObj['address']
            port = serverObj['port']

            print(f"Connecting to {host}:{port}")
            self.sock.connect((host, port))

        except:
            print('Failed to find server...')


    def sendHeader(self, msgLen):
        sendLen = str(msgLen).encode(ENCODING)
        #Add padding to make lenght of header correct
        sendLen += b' '*(HEADER_SIZE-len(sendLen))
        self.sock.send(sendLen)

    def sendData(self, msg):
        #print(f'[SENDING] {msg}')
        message = msg.encode(ENCODING)
        sendLen = str(len(message)).encode(ENCODING)
        #Add padding to make lenght of header correct
        sendLen += b' '*(HEADER_SIZE-len(sendLen))
        message = sendLen + message
        self.sock.sendall(message)
    
    def recResponse(self):
        msgLen = self.sock.recv(HEADER_SIZE).decode(ENCODING)
        # Can only be converted to int if it exists
        if msgLen:
            if msgLen == DISCONNECT:
                self.close()
                return 
            msgLen = int(msgLen)
            try:
                lenRead = 0
                finalResp = ''
                while lenRead < msgLen:
                    resp = self.sock.recv(msgLen-lenRead).decode(ENCODING)
                    lenRead += len(resp)
                    #print(len(resp))
                    finalResp += resp
                finalResp = json.loads(finalResp)
            except JSONDecodeError:
                return None
            #print(f'[STATUS] {resp["status"]}')
            if finalResp["status"] == "OK":
                #print(f'[RESPONSE]: {resp["data"]}')
                return finalResp["data"]
            else:
                return None

    def insert(self, key, val):
        req = {
            "method": "insert",
            "key": key,
            "value": val
        }
        self.sendData(json.dumps(req))
        return self.recResponse()

    def lookup(self, key):
        req = {
            "method": "lookup",
            "key": key
        }
        self.sendData(json.dumps(req))
        return self.recResponse()

    def remove(self, key):
        req = {
            "method": "remove",
            "key": key
        }
        self.sendData(json.dumps(req))
        return self.recResponse()

    def scan(self, regex):
        req = {
            "method": "scan",
            "regex": regex
        }
        self.sendData(json.dumps(req))
        return self.recResponse()

    def close(self):
        print("Closing connection...")
        self.sock.send(DISCONNECT.encode(ENCODING))
        self.sock.close()
