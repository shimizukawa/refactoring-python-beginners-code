"""
ISBN Converter for Python3
LICENSE: GPLv3
"""

import sys


def char2digit(x):
    if x == 'X':
        return 10
    return int(x)


def calc_isbn10_checkdigit(isbn10):
    """calc the check-digit for isbn10"""
    cdigit = sum((10 - i) * x for i,x in enumerate(isbn10[:9]))
    cdigit = 11 - (cdigit % 11)
    return cdigit


def main(args):
    # remove '-' characters from args[0]
    # Note: Anywhere, Any numbers of Hyphen can be accepted.
    isbn = args[0].replace("-", "")

    # ISBN10 validation
    if len(isbn) != 10:
        print(isbn, "is not ISBN10 obviously.")
        sys.exit(0)

    # check for isbn[0:9] which is the first 9 numbers
    # Note: Strictly check the numbers.
    if not isbn[:9].isdigit():
        print("Error: Not a number is included in the 9 numbers.")
        sys.exit(0)

    # check for isbn[9] which is the checkdigit
    # Note: Strictly check the number.
    if not (isbn[9].isdigit() or isbn[9] == 'X'):
        print("Error: Not a number or X is included in the checkdigit.")
        sys.exit(0)

    # calc and check the checkdigit
    iisbn = [char2digit(x) for x in isbn]
    cdigit = calc_isbn10_checkdigit(iisbn)

    if cdigit != iisbn[9]:
        print("Error: Invalid checkdigit.")
        sys.exit(0)

    # calc new(for ISBN13) checkdigit
    ncdigit = 9 * 1 + 7 * 3 + 8 * 1
    for idx in range(4):
        ncdigit += 3 * iisbn[idx * 2] + iisbn[idx * 2 + 1]

    ncdigit += 3 * iisbn[8]
    ncdigit = 10 - (ncdigit % 10)

    # result output
    print("ISBN10:", isbn);
    print("ISBN13:", "978{0}{1}".format(isbn[:9], ncdigit))


def test():
    """run by

    $ python -c "import ISBNConverter as c; c.test()"

    """
    from unittest import mock

    #expect SUCCESS
    with mock.patch('builtins.print'):
        main(['4048686291'])
        print.assert_has_calls([mock.call('ISBN10:','4048686291'),
                                mock.call('ISBN13:','9784048686297')])

    #expect length mismatch ERROR
    with mock.patch('builtins.print'):
        try:
            main(['404868629100'])
        except SystemExit:
            pass
        print.assert_called_once_with(
                '404868629100','is not ISBN10 obviously.')

    #expect almost number only ERROR
    with mock.patch('builtins.print'):
        try:
            main(['4O48686291'])
        except SystemExit:
            pass
        print.assert_called_once_with(
                'Error: Not a number is included in the 9 numbers.')

    #expect ISBN10 check digit is number or X ERROR
    with mock.patch('builtins.print'):
        try:
            main(['404868629Z'])
        except SystemExit:
            pass
        print.assert_called_once_with(
                'Error: Not a number or X is included in the checkdigit.')

    #expect ISBN10 check digit ERROR
    with mock.patch('builtins.print'):
        try:
            main(['4048686292'])
        except SystemExit:
            pass
        print.assert_called_once_with('Error: Invalid checkdigit.')

    print('ok')


if __name__ == '__main__':
    main(sys.argv[1:])
