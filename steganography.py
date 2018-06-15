# -*- coding: utf-8 -*-
from PIL import Image

def tt(c):
    if type(c) == type(''):
        c = ord(c)
    r = bin(c)[2:]
    return '0'*(8-len(r))+r

# byte OOOOOOOO
#       | |  |
#       | |  +------------------+
#       | +----------+          |
#       +--+         |          |
#          |         |          |
# R XXXXXXOO G XXXXXOOO B XXXXXOOO
def dot_put_byte(dot, b):
    return chr((ord(dot[0])&252)+(ord(b)>>6))+chr((ord(dot[1])&248)+(ord(b)>>3&7))+chr((ord(dot[2])&248)+(ord(b)&7))

def dot_get_byte(dot):
    return chr(((ord(dot[0])&3)<<6)+((ord(dot[1])&7)<<3)+(ord(dot[2])&7))

# f1: 'RGB'
# f2: 'L'
# same size
def put_image(f1, f2):
    im1 = Image.open(f1)
    im2 = Image.open(f2)
    im3 = Image.new('RGB', im1.size)
    b1 = im1.tobytes()
    b2 = im2.tobytes()
    b3 = ''.join(map(lambda i:dot_put_byte(b1[3*i:3*i+3], b2[i]), range(len(b2))))
    im3.frombytes(b3)
    ext = f1[f1.rfind('.'):]
    f3 = f1.replace(ext, '.put'+ext)
    im3.save(f3)

def get_image(f1):
    im1 = Image.open(f1)
    im2 = Image.new('L', im1.size)
    b1 = im1.tobytes()
    b2 = ''.join(map(lambda i:dot_get_byte(b1[i:i+3]), range(0, len(b1), 3)))
    im2.frombytes(b2)
    ext = f1[f1.rfind('.'):]
    f2 = f1.replace(ext, '.get'+ext)
    im2.save(f2)
