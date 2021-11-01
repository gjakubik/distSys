import sys
import time
from HashTableClient import HashTableClient

def testPairs(client):
    numOps       = 0
    totTime      = 0.0
    fastOp       = 10000.0
    slowOp       = 0.0
    title        = "\nTesting insert and delete pairs..."

    while numOps < 1020:
        start = time.perf_counter()
        client.insert(str(numOps), numOps*2)
        client.remove(str(numOps))

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
        print("Usage: python3 TestOutliers.py HOSTNAME PORTNUM")
        return

    PORT   = int(sys.argv[2])
    SERVER = sys.argv[1]

    print("\nStarting client...")
    client = HashTableClient()
    client.connSock(SERVER, PORT)
    
    printResult(testPairs(client))

    client.close()


if __name__ == "__main__":
    main()