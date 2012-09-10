"""
ISBN Converter for Python3
LICENSE: GPLv3
"""

import sys


def main(args):
    # remove '-' characters from args[0]
    # Note: Anywhere, Any numbers of Hyphen can be accepted.
    isbn = args[0].replace("-", "")

    # ISBN10 validation
    if len(isbn) != 10:
        print(isbn, "is not ISBN10 obviously.")
        sys.exit(0)

    # String to char to int conversion
    cisbn = isbn
    iisbn = [None] * 10;

    # check for iisbn[0:9] which is the first 9 numbers
    # Note: Strictly check the numbers.
    for idx in range(9):
        if not cisbn[idx].isdigit():
            print("Error: Not a number is included in the 9 numbers.")
            sys.exit(0)
        iisbn[idx] = int(cisbn[idx])

    # check for iisbn[9] which is the checkdigit
    # Note: Strictly check the number.
    if cisbn[9] == 'X':
        iisbn[9] = 10
    else:
        iisbn[9] = int(cisbn[9])
        if not cisbn[9].isdigit():
            print("Error: Not a number or X is included in the checkdigit.")
            sys.exit(0)

    # calc and check the checkdigit
    cdigit = 0;
    for idx in range(9):
        cdigit += (10 - idx) * iisbn[idx]

    cdigit = cdigit % 11
    cdigit = 11 - cdigit

    if cdigit != iisbn[9]:
        print("Error: Invalid checkdigit.")
        sys.exit(0)

    # calc new(for ISBN13) checkdigit
    ncdigit = 9 * 1 + 7 * 3 + 8 * 1
    for idx in range(4):
        ncdigit += 3 * iisbn[idx * 2] + iisbn[idx * 2 + 1]

    ncdigit += 3 * iisbn[8]
    ncdigit %= 10
    ncdigit = 10 - ncdigit

    # Convert int to String for ISBN13 checkdigit
    lastx = str(ncdigit)

    # result output
    print("ISBN10:", isbn);
    print("ISBN13:", "978" + isbn[:9] + lastx)


if __name__ == '__main__':
    main(sys.argv[1:])
