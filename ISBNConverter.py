"""
ISBN Converter for Python3
LICENSE: GPLv3
"""

import sys
from itertools import cycle


def calc_isbn10_checkdigit(isbn10):
    """calc the check-digit for isbn10"""
    cdigit = sum((10 - i) * x for i,x in enumerate(map(int, isbn10[:9])))
    cdigit = 11 - (cdigit % 11)
    return "0123456789X"[cdigit]

def calc_isbn13_checkdigit(isbn13):
    """calc the check-digit for isbn13"""
    ncdigit = sum(x * y for x, y in zip(map(int, isbn13[:12]), cycle([1,3])))
    ncdigit = 10 - (ncdigit % 10)
    return "0123456789X"[ncdigit]


def validate_isbn10(isbn10):
    """check the checkdigit"""

    # ISBN10 validation
    if len(isbn10) != 10:
        raise ValueError("{0} is not ISBN10 obviously.".format(isbn10))

    # check for isbn10[0:9] which is the first 9 numbers
    # Note: Strictly check the numbers.
    if not isbn10[:9].isdigit():
        raise ValueError("Error: Not a number is included in the 9 numbers.")

    # check for isbn10[9] which is the checkdigit
    # Note: Strictly check the number.
    if not (isbn10[9].isdigit() or isbn10[9] == 'X'):
        raise ValueError("Error: Not a number or X is included in the checkdigit.")

    cdigit = calc_isbn10_checkdigit(isbn10)
    if cdigit != isbn10[9]:
        raise ValueError("Error: Invalid checkdigit.")

    return True


def make_isbn13_from_isbn10(isbn10):
    """make new ISBN13 from ISBN10"""
    isbn12 = '978' + isbn10[:9]
    cdigit = calc_isbn13_checkdigit(isbn12)
    return isbn12 + cdigit


def convert_isbn10_to_isbn13(isbn10):
    # remove '-' characters from isbn10
    # Note: Anywhere, Any numbers of Hyphen can be accepted.
    isbn10 = isbn10.replace("-", "")

    # calc and check the checkdigit
    validate_isbn10(isbn10)

    # calc new(for ISBN13) checkdigit
    isbn13 = make_isbn13_from_isbn10(isbn10)

    return isbn13


def test():
    """run by

    $ python -c "import ISBNConverter as c; c.test()"

    """
    #expect SUCCESS
    assert convert_isbn10_to_isbn13('4048686291') == '9784048686297'

    #expect length mismatch ERROR
    try:
        convert_isbn10_to_isbn13('404868629100')
    except ValueError as e:
        assert str(e) == '404868629100 is not ISBN10 obviously.'

    #expect almost number only ERROR
    try:
        convert_isbn10_to_isbn13('4O48686291')
    except ValueError as e:
        assert str(e) == 'Error: Not a number is included in the 9 numbers.'

    #expect ISBN10 check digit is number or X ERROR
    try:
        convert_isbn10_to_isbn13('404868629Z')
    except ValueError as e:
        assert str(e) == 'Error: Not a number or X is included in the checkdigit.'

    #expect ISBN10 check digit ERROR
    try:
        convert_isbn10_to_isbn13('4048686292')
    except ValueError as e:
        assert str(e) == 'Error: Invalid checkdigit.'

    print('ok')


if __name__ == '__main__':
    isbn13 = convert_isbn10_to_isbn13(sys.argv[1])

    # result output
    print("ISBN10:", isbn10)
    print("ISBN13:", isbn13)
