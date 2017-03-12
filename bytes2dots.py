#!/usr/bin/env python3

UNICODE_BRAILLE_BASE = 0x2800

def int2bits(v):
    """
    >>> int2bits(25)
    [0, 0, 0, 1, 1, 0, 0, 1]
    """
    assert 0 <= v <= 255
    return [(v >> i) & 1 for i in range(7, -1, -1)]

def bits2int(v):
    """
    >>> bits2int([0,0,0,0, 1,1,1,1])
    15
    """
    assert len(v) == 8
    return sum((bit << (7-i) for i, bit in enumerate(v)))

# ISO/TR 1154 numbers the braille dots 1 to 8 placed, as shown -->    | 1 4 |
# Unicode also uses this numbering scheme                             | 2 5 |
# e.g. U+2813 BRAILLE PATTERN DOTS-125 has dots 1, 2 and 5 raised     | 3 6 |
#                                                                     | 7 8 |

# The following mappings number the braille dots from 0 to 7, to align with
# the powers of 2 corresponding to bits in a byte

bitpos2braillepos = {
    4:0, 0:3,
    5:1, 1:4,
    6:2, 2:5,
    7:6, 3:7,
}

braillepos2bitpos = {
    0:4, 3:0,
    1:5, 4:1,
    2:6, 5:2,
    6:7, 7:3,
}

def byte2dots(byte):
    """
    >>> [byte2dots(i) for i in (0xff, 0xf0, Ox0f, 0x00, 0x31)]
    ['⣿', '⡇', '⢸', ' ','⠋']
    """
    bits = int2bits(byte)
    bits.reverse()
    dots = [bits[braillepos2bitpos[i]] for i in range(8)]
    dots.reverse()

    braillechar = chr(UNICODE_BRAILLE_BASE + bits2int(dots))
    return braillechar

def bytes2dots(s):
    """
    >>> single_bits = b'\x01\x02\x04\x08\x10\x20\x40\x80'
    >>> complements = ((~ byte) & 255 for byte in single_bits)
    >>> bytes2dots(single_bits)
    '⠈ ⠐ ⠠ ⢀ ⠁ ⠂ ⠄ ⡀'
    >>> bytes2dots(complements)
    '⣷ ⣯ ⣟ ⡿ ⣾ ⣽ ⣻ ⢿'
    """
    return ' '.join(byte2dots(byte) for byte in s)


if __name__ == '__main__':
    #print(bytes2dots(b'\xff\xf3\xf1\xf0\x0f\x1f\x3f\xff'))
    #print(bytes2dots(b'\x01\x02\x04\x08\x10\x20\x40\x80'))

    print('  ' + ''.join('%2x' % i for i in range(16)))
    for i in range(0, 256, 16):
        print('%02x' % i, end=' ')
        print( bytes2dots(i+j for j in range(16)) )
