import sys
from ClusterClient import ClusterClient, ClientError, ServerError

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 TestBasics.py PROJECT_NAME N K")
        return

    print("\nStarting client...")
    try:
        client = ClusterClient(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    except ServerError:
        print("Connection failed. Check servers and try again")
        return

    print("\nMaking sure you cant delete nothing...")
    for i in range(10):
        try:
            val = client.remove(str(i))
            if val:
                raise AssertionError
        # ClientError expected, Any other error will make test fail
        except ClientError:
            pass

    print("\nInserting a large amount of numbers...")
    for i in range(10):
        client.insert(str(i), i*3)

    print("\nInserting a list...")
    client.insert("list", [1, 2, 3, 4, 5])

    print("\nInserting a dict...")
    client.insert("dict", {str(i): i*2 for i in range(10)})

    print("\nChecking values...")
    for i in range(10):
        assert(client.lookup(str(i)) == i*3)
        assert(client.lookup("dict")[str(i)] == i*2)
    
    assert(client.lookup("list") == [1, 2, 3, 4, 5])

    print("\nTesting scan...")
    for match in client.scan("[0-9]{2}7"):
        assert(str(match)[2] == '7')

    print("\nTesting delete...\n")
    for i in range(10):
        assert(client.remove(str(i)) == i*3)
        try:
            val = client.lookup(str(i))
            if val:
                raise AssertionError
        # ClientError expected, Any other error will make test fail
        except ClientError:
            pass


    client.close()


if __name__ == "__main__":
    main()