# binary2text

A silly experiment to show how various string escape and str->str encodings behave

```
$ python3 binary2text.py 
Encoding             Result                   Length inc
HTML escape          Hello world!                      0
URL quote            Hello%20world%21                  4
URL quote plus       Hello+world%21                    2
XML escape           Hello world!                      0
XML quote attribute  "Hello world!"                    2
reference            Hello world!                      0
base64               SGVsbG8gd29ybGQh                  4
  standard           SGVsbG8gd29ybGQh                  4
  urlsafe            SGVsbG8gd29ybGQh                  4
base32               JBSWY3DPEB3W64TMMQQQ====         12
base16               48656C6C6F20776F726C6421         12
Ascii85              87cURD]j7BEbo80                   3
base85               NM&qnZy<MXa%^NF                   3
quoted printable     Hello world!                      0
ZeroMQ Z85           nm=QNzY<mxA+]nf                   3
base36               102iefafi4ncbng8ax4               7
base26               nmoqgbeyffssrmplfbrs              8
```
