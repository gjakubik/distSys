from HashTable import HashTable

def main():
    print('Initializing...')
    ht = HashTable()
    print('Inserting...')
    ht.insert('a', 'actuary')
    ht.insert('ba', 'banker')
    ht.insert('c', 'cashier')
    ht.insert('d', 'driver')

    print('Using lookup...')
    print(ht.lookup('a'))
    print(ht.lookup('ba'))
    print(ht.lookup('c'))

    print('Deleting value')
    print(ht.remove('d'))

    print('Scanning for matches...')
    print(ht.scan('a'))


if __name__ == '__main__':
    main()