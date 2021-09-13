import Test1
import Test2
import Test3
import Test4
import Test5
import Test6
import Test7
import Test8
import Test9
import Test10

def main():

    print("\nTest 1: Trivial Function Call")
    Test1.main()

    print("\nTest 2: Create/Delete File in Home Dir")
    Test2.main()

    print("\nTest 2: Create/Delete File in /tmp")
    Test3.main()

    print("\nTest 4: Get Current Wall Clock Time")
    Test4.main()

    print("\nTest 5: Insert Item Into Python Dict")
    Test5.main()

    print("\nTest 6: Make and Close TCP Connection to Google")
    Test6.main()

    print("\nTest 7: Make an HTTP Connection to Github and read back HTML")
    Test7.main()

    print("\nTest 8: Open a Large JSON File and Parse it")
    Test8.main()

    print("\nTest 9: Use 'scandir' to 'stat' Each Item in Home Dir")
    Test9.main()

    print("\nTest 10: Run ls -l as a Subprocess")
    Test10.main()

if __name__ == "__main__":
    main()