import time
import hashlib

from HashTableClient import HashTableClient

class ServerError(Exception):
    '''Raised when the server doesn't respond'''
    pass

class ClientError(Exception):
    '''Raised when the client sends a bad request'''
    pass

class ClusterClient():
    # Return 0 on failure, 1 on success
    def __init__(self, name, N, K):
        self.name = name
        self.N    = N
        self.K    = K

        #Create a client object for each server
        self.servers = []
        for i in range(N):
            server = HashTableClient()
            port = server.connSock(f'{name}-{i}')
            # If returned port is 0, connection failed, so the full init fails
            if port != 0:
                self.servers.append(server)
            else:
                return 0

        return 1
    
    # findservers will take a key and return the list of server indicies
    # TODO: Possible performance benefit from memoizing hashes if same keys are used often
    def findServers(self, key):
        H = hashlib.sha256()
        H.update(key.encode())
        S = int.from_bytes(H.digest(), 'big') % self.N
        indicies = [S]
        for i in range(self.K):
            if i == 0:
                continue
            indicies.append( (S+i) % self.N )

        return indicies
        
    # Find the servers that correspond to the key then insert into all
    def insert(self, key, val):
        for i in self.findServers(key):
            resp = self.servers[i].insert(key, val)
            # If response was bad, we should try to reestablish a new connection
            if resp["status"] == "Bad Response":
                self.servers[i] = HashTableClient()
                self.servers[i].connSock(f'{self.name}-{i}')
                resp = self.servers[i].insert(key, val)
                # If bad response again, stop trying
                if resp["status"] == "Bad Response":
                    raise ServerError
            # If request was bad, then it was an invalid op or invalid key, so client side issue
            elif resp["status"] == "Bad Request" or resp["status"] == "Key not found":
                raise ClientError

        return resp["value"]

    # TODO: lookup in possible places until value is found
    def lookup(self, key):
        for i in self.findServers(key):
            resp = self.servers[i].lookup(key)
            # If response was bad, we should try to reestablish a new connection
            if resp["status"] == "Bad Response":
                self.servers[i] = HashTableClient()
                self.servers[i].connSock(f'{self.name}-{i}')
                resp = self.servers[i].lookup(key)
                # If bad response again, stop trying
                if resp["status"] == "Bad Response":
                    raise ServerError
            # If request was bad, then it was an invalid op or invalid key, so client side issue
            elif resp["status"] == "Bad Request" or resp["status"] == "Key not found":
                raise ClientError
        # return None when val not found
        return resp["value"]


    # Remove from all servers corresponding to key
    def remove(self, key):
        for i in self.findServers(key):
            resp = self.servers[i].remove(key)
            if resp["status"] == "Bad Response":
                self.servers[i] = HashTableClient()
                self.servers[i].connSock(f'{self.name}-{i}')
                resp = self.servers[i].remove(key)
                # If bad response again, stop trying
                if resp["status"] == "Bad Response":
                    raise ServerError
            # If request was bad, then it was an invalid op or invalid key, so client side issue
            elif resp["status"] == "Bad Request" or resp["status"] == "Key not found":
                raise ClientError
        
        return resp["value"]

    # Find the result for each server and concatenate them
    def scan(self, regex):
        results = []
        for i in range(self.K):
            resp = self.servers[i].scan(regex)
            if resp["status"] == "Bad Response":
                self.servers[i] = HashTableClient()
                self.servers[i].connSock(f'{self.name}-{i}')
                resp = self.servers[i].scan(regex)
                # If bad response again, stop trying
                if resp["status"] == "Bad Response":
                    raise ServerError
            # If request was bad, then it was an invalid op or invalid key, so client side issue
            elif resp["status"] == "Bad Request" or resp["status"] == "Key not found":
                raise ClientError

            results += resp["matches"]
        
        return results

    def close(self):
        print("Closing connections...")
        
        for conn in self.servers:
            conn.close()