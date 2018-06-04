# -*- coding: utf-8 -*-
from struct import pack, unpack

def en(c):
    if len(c) == 1:
        c += ' '
    elif len(c) > 2:
        raise Exception('only 2 characters')
    r = str(unpack('>d', '@'+c+'@\xff\xff\xff\xff')[0])
    for i in range(1, len(r)):
        if pack('>d', float(r[:i]))[:4] == '@'+c+'@':
            return r[:i]

def de(f):
    r = pack('>d', float(f))
    if r[0] == '@' and r[3] == '@':
        return r[1:3]                                                                                                  
    else:
        return ''

def encode(s):
    if type(s) != type(''):
        raise TypeError
    return '\n'.join(map(lambda i:en(s[i:i+2]), range(0, len(s), 2)))

def decode(s):
    if type(s) == type(0.0) or type(s) == type(0):
        return de(s)
    elif type(s) == type('') or type(s) == type(u''):
        return ''.join(map(de, s.split()))                                                                             
    raise TypeError
