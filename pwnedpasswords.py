# -*- coding: utf-8 -*-
import requests
from sys import argv
from hashlib import sha1

def chk(pw):
    a = sha1()
    a.update(pw)
    s = a.hexdigest().upper()
    web = requests.get('https://api.pwnedpasswords.com/range/'+s[:5], headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'})
    d = dict(i.split(':') for i in web.content.split())
    return int(d[s[5:]]) if s[5:] in d else 0

if __name__ == '__main__':
    print chk(argv[1])
