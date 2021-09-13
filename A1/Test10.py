import subprocess
import time

def main():
    numOps = 400
    totTime = 0.0
    fastOp = 10000.0
    slowOp = 0.0

    for i in range(numOps):
        start = time.perf_counter()

        # Start timed ops
        subprocess.run(["ls", "/escnfs/home/gjakubik", "-l"], capture_output=True)
        # End timed ops

        opTime = time.perf_counter() - start
        totTime += opTime

        fastOp = opTime if opTime < fastOp else fastOp
        slowOp = opTime if opTime > slowOp else slowOp
    
    print(f'+{"-"*89}+')
    print(f'| {"Num Ops":<7} | {"Total Time (s)":<16} | {"Average Op Time (s)":<20} | {"Slowest Op (s)":<16} | {"Fastest Op (s)":<16} |')
    print(f'| {" "*7} | {" "*16} | {" "*20} | {" "*16} | {" "*16} |')
    print(f'| {numOps:<7} | {totTime:<16.12} | {totTime/numOps:<20.15} | {slowOp:<16.10} | {fastOp:<16.10} |')
    print(f'+{"-"*89}+')


if __name__ == "__main__":
    main()