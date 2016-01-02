#!/usr/bin/env python3
"""
Experimenting with string escaping and byte string -> text encodings.
"""

import base64
import html
import quopri
import string
import urllib.parse
import xml.sax.saxutils

#import basin
import zmq.utils.z85


# Mnemonic schemes
# BIP 39        https://pypi.python.org/pypi/mnemonic/0.12
#               https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
# mnemonicode   https://pypi.python.org/pypi/mnemonicode/1.2.0
#               https://web.archive.org/web/20101031205747/http://www.tothink.com/mnemonic/
# OTP           https://labix.org/python-otp
#               https://www.ietf.org/rfc/rfc2289.txt
# PGP word list https://pypi.python.org/pypi/hex2words
#               https://en.wikipedia.org/wiki/PGP_word_list
#
data = 'Hello world!'
headings = ('Encoding', 'Result', 'Length inc')
fmtstr = '{0:<20} {1:<24} {2:>10}'

def basin_encode(alphabet, n):
    """
    Encode integer value `n` using `alphabet`. The resulting string will be a
    base-N representation of `n`, where N is the length of `alphabet`.
    
    """
    
    if not (isinstance(n, int) or isinstance(n, long)):
        raise TypeError('value to encode must be an int or long')
    r = []
    base  = len(alphabet)
    while n >= base:
        r.append(alphabet[n % base])
        n = n // base
    r.append(str(alphabet[n % base]))
    r.reverse()
    return ''.join(r).encode('ascii')

def basin_bytestring_to_integer(bytes):
    """Return the integral representation of a bytestring."""
    
    n = 0
    for (i, byte) in enumerate(bytes):
        n += byte << (8 * i)
    return n

def base36_encode(s):
    return basin_encode(string.digits + string.ascii_lowercase,
                        basin_bytestring_to_integer(s))

def base26_encode(s):
    return basin_encode(string.ascii_lowercase,
                        basin_bytestring_to_integer(s))

str_encodings = [
    ('HTML escape',         html.escape),
    # http://user:pass@example.com:80/path/index.html;param=foo?q=bar
    ('URL quote',           urllib.parse.quote),
    ('URL quote plus',      urllib.parse.quote_plus),
    ('URL quote',           urllib.parse.quote),
    ('XML escape',          xml.sax.saxutils.escape),
    ('XML quote attribute', xml.sax.saxutils.quoteattr),
    
    ]

byte_encodings = [
    ('reference',           bytes),
    ('base64',              base64.b64encode),
    ('  standard',          base64.standard_b64encode),
    ('  urlsafe',           base64.urlsafe_b64encode),
    ('base32',              base64.b32encode),
    ('base16',              base64.b16encode),
    ('Ascii85',             base64.a85encode),
    ('base85',              base64.b85encode),
    ('quoted printable',    quopri.encodestring),
    # Only works for inputs with length divisble by 4
    ('ZeroMQ Z85',          zmq.utils.z85.encode),
    ('base36',              base36_encode),
    ('base26',              base26_encode),
    ]

print(fmtstr.format(*headings))

for label, enc_func in str_encodings:
    data_enc = enc_func(data)
    print(fmtstr.format(label, data_enc, len(data_enc) - len(data)))

for label, enc_func in byte_encodings:
    data_utf8 = data.encode('utf-8')
    data_encb = enc_func(data_utf8)
    data_enc = data_encb.decode('ascii')
    print(fmtstr.format(label, data_enc, len(data_enc) - len(data_utf8)))
