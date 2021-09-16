import re

class HashTable():
    def __init__(self):
        self.d = {}

    def insert(self, key, val):
        self.d[key] = val

    def lookup(self, key):
        return self.d[key]

    def remove(self, key):
        return self.d.pop(key)

    def scan(self, regex):
        print(f"Compiling regex: {regex}")
        r = re.compile(regex)
        matches = []
        for key in self.d.keys():
            print(f"searching key: {key}")
            match = (r.search(str(key)) != None)
            print("adding key")
            if match: matches.append(key)

        return matches
