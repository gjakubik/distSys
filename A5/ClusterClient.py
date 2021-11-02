import time

import HashTableClient

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
            if port:
                self.servers.append(server)
            else:
                return 0

        return 1
    
    # TODO: findserver will take a key and return the index of the server
    # to be used for that key
    def findServer(key):
        pass

    # Invoke each of insert, lookup and remove by
    # finding correct server index and passing operation to that handler
    def insert(self, key, val):
        self.servers[self.findServer(key)].insert(key, val)

    def lookup(self, key):
        self.servers[self.findServer(key)].lookup(key)

    def remove(self, key):
        self.servers[self.findServer(key)].remove(key)

    # TODO: Scan must find the result for each server and concatenate them
    def scan(self, regex):
        pass

    def close(self):
        print("Closing connections...")
        
        for conn in self.servers:
            conn.close()