import re

class HashTable():
    def __init__(self):
        self.d = {}
        self.txns = 0
        self.txn = None

    def insert(self, key, val):
        self.d[key] = val

    def lookup(self, key):
        return self.d[key]

    def remove(self, key):
        try:
            return self.d.pop(key)
        except:
            return None

    def scan(self, regex):
        r = re.compile(str(regex))
        matches = []
        for key in self.d.keys():
            match = (r.search(str(key)) != None)
            if match: matches.append(key)

        return matches
