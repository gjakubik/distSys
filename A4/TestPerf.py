import sys
import time
from HashTableClient import HashTableClient

def testInsert(client):
    numOps       = 0
    totTime      = 0.0
    overallStart = time.perf_counter()
    title        = "\nInserting a large amount of numbers..."

    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.insert(str(numOps), numOps*2)

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

    tPut = numOps/totTime
    return (title, numOps, totTime, tPut, 1/tPut)

def testLookup(client):
    numOps       = 0
    totTime      = 0.0
    overallStart = time.perf_counter()
    title        = "\nLooking up a large amount of numbers..."

    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.lookup(str(numOps))

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

    tPut = numOps/totTime
    return (title, numOps, totTime, tPut, 1/tPut)


def testScan(client):
    numOps       = 0
    totTime      = 0.0
    overallStart = time.perf_counter()
    title        = "\nScanning for regexes..."

    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.scan(str(numOps))

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

    tPut = numOps/totTime
    return (title, numOps, totTime, tPut, 1/tPut)


def testRemove(client):
    numOps       = 0
    totTime      = 0.0
    overallStart = time.perf_counter()
    title        = "\nRemoving as many numbers as possible..."
    
    while time.perf_counter() - overallStart < 3:
        start = time.perf_counter()
        client.remove(str(numOps))

        numOps += 1
        opTime = time.perf_counter() - start
        totTime += opTime

    tPut = numOps/totTime
    return (title, numOps, totTime, tPut, 1/tPut)


def printResult(res, port):
    print(f'[{port}]: {res[0]}')
    print(f'+{"-"*74}+')
    print(f'| {"Num Ops":<7} | {"Total Time (s)":<16} | {"Thoroughput (ops/s)":<20} | {"Latency (s/op)":<20} |')
    print(f'| {" "*7} | {" "*16} | {" "*20} | {" "*20} |')
    print(f'| {res[1]:<7} | {res[2]:<16.12} | {res[3]:<20.15} | {res[4]:<20.15} |')
    print(f'+{"-"*74}+')

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 TestPerf.py PROJECT_NAME")
        return

    client = HashTableClient()
    port = client.connSock(sys.argv[1])
    print(f"\nPort {port} client statistics: \n")

    # Server wasnt found if port 0
    if port == 0: return
    results = []

    results.append(testInsert(client))
    results.append(testLookup(client))
    results.append(testScan(client))
    results.append(testRemove(client))
    
    for res in results:
        printResult(res, port)

    client.close()


if __name__ == "__main__":
    main()