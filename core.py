# -*- coding: utf-8 -*-
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

# notice: match ip like 1111.222.33.444 => 111.22.33.44
import re
match_ip = re.compile(r'((?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))')

from locale import getdefaultlocale
LOCAL = getdefaultlocale()[1]

from bs4 import BeautifulSoup
bs = lambda i:BeautifulSoup(i, 'html.parser')

def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

if __name__ == '__main__':
    pass

'''
exit()
python
'''
