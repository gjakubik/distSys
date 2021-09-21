import sys
import time
from HashTableClient import HashTableClient

def testInsert(client):
    numOps       = 0
    totTime      = 0.0
    fastOp       = 10000.0
    slowOp       = 0.0
    overallStart = time.perf_counter()
    title        = "\nInserting a large amount of numbers..."

    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.insert(numOps, numOps*2)

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

        fastOp = opTime if opTime < fastOp else fastOp
        slowOp = opTime if opTime > slowOp else slowOp

    return (title, numOps, totTime, totTime/numOps, slowOp, fastOp)

def testLookup(client):
    numOps       = 0
    totTime      = 0.0
    fastOp       = 10000.0
    slowOp       = 0.0
    overallStart = time.perf_counter()
    title        = "\nLooking up a large amount of numbers(while loop)..."

    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.lookup(numOps)

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

        fastOp = opTime if opTime < fastOp else fastOp
        slowOp = opTime if opTime > slowOp else slowOp

    return (title, numOps, totTime, totTime/numOps, slowOp, fastOp)


def testScan(client):
    numOps       = 0
    totTime      = 0.0
    fastOp       = 10000.0
    slowOp       = 0.0
    overallStart = time.perf_counter()
    title        = "\nScanning for regexes..."

    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.scan(numOps)

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

        fastOp = opTime if opTime < fastOp else fastOp
        slowOp = opTime if opTime > slowOp else slowOp

    return (title, numOps, totTime, totTime/numOps, slowOp, fastOp)


def testRemove(client):
    numOps       = 0
    totTime      = 0.0
    fastOp       = 10000.0
    slowOp       = 0.0
    overallStart = time.perf_counter()
    title        = "\nRemoving as many numbers as possible..."
    
    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.remove(numOps)

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

        fastOp = opTime if opTime < fastOp else fastOp
        slowOp = opTime if opTime > slowOp else slowOp

    return (title, numOps, totTime, totTime/numOps, slowOp, fastOp)


def printResult(res):
    print(res[0])
    print(f'+{"-"*89}+')
    print(f'| {"Num Ops":<7} | {"Total Time (s)":<16} | {"Average Op Time (s)":<20} | {"Slowest Op (s)":<16} | {"Fastest Op (s)":<16} |')
    print(f'| {" "*7} | {" "*16} | {" "*20} | {" "*16} | {" "*16} |')
    print(f'| {res[1]:<7} | {res[2]:<16.12} | {res[3]:<20.15} | {res[4]:<16.10} | {res[5]:<16.10} |')
    print(f'+{"-"*89}+')

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 TestPerf.py HOSTNAME PORTNUM")
        return

    PORT   = int(sys.argv[2])
    SERVER = sys.argv[1]

    print("\nStarting client...")
    client = HashTableClient()
    client.connSock(SERVER, PORT)
    results = []

    results.append(testInsert(client))
    results.append(testLookup(client))
    results.append(testScan(client))
    results.append(testRemove(client))
    
    for res in results:
        printResult(res)

    client.close()


if __name__ == "__main__":
    main()