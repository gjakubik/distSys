import sys
from HashTableClient import HashTableClient

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 TestBasics.py PROJECT_NAME")
        return

    print("\nStarting client...")
    client = HashTableClient()
    client.connSock(sys.argv[1])

    print("\nMaking sure you cant delete nothing...")
    for i in range(10):
        res = client.remove(str(i))
        assert(res["value"] == None)

    print("\nInserting a large amount of numbers...")
    for i in range(10):
        client.insert(str(i), i*3)

    print("\nInserting a list...")
    client.insert("list", [1, 2, 3, 4, 5])

    print("\nInserting a large dict...")
    client.insert("dict", {str(i): i*2 for i in range(1000)})

    print("\nChecking values...")
    try:
        for i in range(10):
            assert(client.lookup(str(i))["value"] == i*3)
            assert(client.lookup("dict")["value"][str(i)] == i*2)
        
        assert(client.lookup("list")["value"] == [1, 2, 3, 4, 5])
    except AssertionError as e:
        print('Test Failed')
        print(e)

    print("\nTesting scan...")
    for match in client.scan("[0-9]{2}7")["matches"]:
        assert(str(match)[2] == '7')

    print("\nTesting delete...\n")
    for i in range(10):
        assert(client.remove(str(i))["value"] == i*3)
        assert(client.lookup(str(i)) == None)


    client.close()


if __name__ == "__main__":
    main()