""" Pickling list of numbers or list of lists/tuples of number (equal length)

    Restrictions: Numbers must be positive. If not they will be
                    pickled as positive. (Will be changed soon)
                  Length of inserted list/tuple couldn't exceed 95
                  Length of word for one number couldn't be zero
                  Length of word for one number couldn't exceed 95
                  (number must be lower than 95**96-1)
    List of integer or long numbers is really huge in JSON
    or native pickling, because they used string representation
    of numbers. Besides lists with same length often has different
    length after pickling. And this behavior can be undesirable
    with updating DataBase storage or forming some data
    structures.

    This method allows to have compatible and fixed-length
    representation of list. It can be used in 2 ways:
    1 - without non-printable character
        In this way one letter is 95 values,
        so word with, for example, five letters can
        represent number not more than 95**5 = 7737809375
    2 - with all octet values (0-255)
        In this way integers or longs number will be
        represented with same number of letters as they
        used number of bytes. This method is more
        compatible, but such byte-string couldn't be saved
        in Data Base text fields.
"""

BYTES = 256
STRING = 95


def num_to_bytes(num, l=5, base=STRING):
    """ Represents given number in bytes-string

    :param num: Given number
    :param l: Fixed length of result string. Default 5
        because 95**5 can represent any integer number.
    :param base: base of calculation. 95 for printable result,
        256 for non-printable bytes.
    :return: bytes-string with length l
    """
    offset = 32 if base == STRING else 0
    minus = True if num < 0 else False
    num = abs(num)
    _num = list()
    while num:
        num, byte = divmod(num, base)
        _num.append(byte)

    num = [chr(offset)] * l
    for n, byte in enumerate(_num):
        byte = chr(byte+offset)
        num[n] = byte
    return ''.join(num)

def bytes_to_num(word, base=STRING):
    """ Computes number from bytes-string

    :param word: Given bytes-string
    :param base: base of calculation. 95 for printable,
        256 for non-printable bytes-string.
    :return: number
    """
    offset = 32 if base == STRING else 0
    res = 0
    for n, symbol in enumerate(word):
        num = (ord(symbol) - offset)*base**n
        res += num
    return res

def dumps(given_list, lens, base=STRING):
    """ Coding given list of numbers or list of lists/tuples of numbers into bytes-string

    :param given_list: must be list of numbers
        like [1532, 343, 3, 0, 2342343234]
        or list of lists/tuples of numbers (equal length)
        like [[12, 2], [2, 4], [12353, 3]]
        or [(123121, 231), (123123, 23), (2, 2)]

    :param lens: tuple of lens of each number of each inserted list/tuple
        where len is number of letter which is enough to represent number
    :param base: base of calculation. 95 for printable result,
        256 for non-printable bytes.
    :return: bytes-string
    """
    if len(lens)>95:
        raise AttributeError('Length of inserted list/tuple exceed 95')
    lens = filter(lambda x: x>0, map(int, lens))
    result = list()
    for item in given_list:
        word = ''
        for n, x in enumerate(item):
            word += num_to_bytes(x, lens[n], base)
        result.append(word)
    l = num_to_bytes(len(lens), 1, STRING)
    _lens = [num_to_bytes(x, 1, STRING) for x in lens]
    _lens = ''.join(_lens)
    pre = l + _lens

    return pre + ''.join(result)

def loads(given_string, base=STRING):
    l = bytes_to_num(given_string[0], STRING)
    _lens = given_string[1:l+1]
    lens = list()
    for byte in _lens:
        lens.append(bytes_to_num(byte, STRING))
    word_len = sum(lens)
    given_string = given_string[l+1:]
    res = list()
    while given_string:
        inserted = list()
        word, given_string = given_string[:word_len], given_string[word_len:]
        _l = 0
        for l in lens:
            inserted.append(word[_l:_l+l])
            _l += l
        inserted = [bytes_to_num(x) for n, x in enumerate(inserted)]
        res.append(inserted)
    return res
