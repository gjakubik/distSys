import time
import hashlib

from HashTableClient import HashTableClient

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
            self.servers[i].insert(key, val)

    # TODO: lookup in possible places until value is found
    def lookup(self, key):
        for i in self.findServers(key):
            val = self.servers[i].lookup(key)
            if  val != None:
                return val["value"]
        # return None when val not found
        return None


    # Remove from all servers corresponding to key
    def remove(self, key):
        for i in self.findServers(key):
            val = self.servers[i].remove(key)
        return val

    # Find the result for each server and concatenate them
    def scan(self, regex):
        results = []
        for server in self.servers:
            results += server.scan(regex)
        
        return results

    def close(self):
        print("Closing connections...")
        
        for conn in self.servers:
            conn.close()