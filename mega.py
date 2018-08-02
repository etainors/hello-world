# -*- coding: utf-8 -*-
import os
from sys import argv

# Windows:
# pip install pycrypto
# http://aka.ms/vcpython27
# https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266
# VCForPython27.msi
from Crypto.Cipher import AES

#def key():
    #arr = list(pw)
    #for i in range(160):
        #arr[i%32] = arr[i%32] ^ enc_xor[i%9]
    #return tuple(arr)

#pw = (110, 89, 114, 88, 97, 64, 57, 81, 63, 49, 38, 104, 67, 87, 77, 92, 57, 40, 55, 51, 49, 66, 112, 63, 116, 52, 50, 61, 33, 107, 51, 46)
#iv = (121, 241, 10, 1, 132, 74, 11, 39, 255, 91, 45, 78, 14, 211, 22, 62)
#enc_xor = (12, 57, 251, 120, 18, 75, 6, 250, 85)

#pwd = key()
#pwd = (237, 31, 76, 32, 11, 53, 19, 152, 6, 178, 96, 86, 59, 61, 56, 118, 240, 17, 180, 117, 15, 58, 26, 74, 94, 253, 11, 190, 103, 85, 75, 68)

pw = '\xed\x1fL \x0b5\x13\x98\x06\xb2`V;=8v\xf0\x11\xb4u\x0f:\x1aJ^\xfd\x0b\xbegUKD'
iv = "y\xf1\n\x01\x84J\x0b'\xff[-N\x0e\xd3\x16>"
def decode_mega(s):
    s = s.replace('-', '+').replace('_', '/')
    while len(s)%4 != 0:
        s += '='
    r = AES.new(pw, AES.MODE_CBC, iv).decrypt(s.decode('base64'))
    while r[-1] = '\x0b' or r[-1] == '\x10':
        r = r[:-1]
    return r

def main(s):
    if s.lower().startswith('mega://enc2?'):
        return 'https://mega.nz/#'+decode_mega(s[12:])
    elif s.lower().startswith('mega://fenc2?'):
        return 'https://mega.nz/#F'+decode_mega(s[13:])
    else:
        return s

if __name__ == '__main__':
    if os.path.isfile(argv[1]):
        a = open(argv[1]).read().split('\n')
        a = map(main, a)
        open(argv[1], 'w').write('\n'.join(a))
    else:
        print main(argv[1])