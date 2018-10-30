# -*- coding: utf-8 -*-
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

# notice: match ip like 1111.222.33.444 => 111.22.33.44
import re
match_ip = re.compile(r'((?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))')

from locale import getdefaultlocale
LOCAL = getdefaultlocale()[1] if getdefaultlocale()[1] else 'UTF-8'# for MAC

from datetime import datetime
datetime.utcnow().isoformat()

from bs4 import BeautifulSoup
bs = lambda i:BeautifulSoup(i, 'html.parser')

def is_int(s):
    try:
        return int(s) == float(s)
    except:
        return False

# check os is windows
from sys import platform
is_win = platform.startswith('win')

# or
from platform import platform
is_win = platform().lower().startswith('win')

# return command output
from subprocess import check_output
from commands import getoutput

# 顯示錯誤資訊
def errmess(n=1):
    from traceback import format_exc
    return '\n'.join(format_exc().split('\n')[-n-1:-1])

import os
from time import sleep
# lock resource
def unlock():
    os.remove('locked')

def lock():
    while True:
        try:
            fd = os.open('locked', os.O_WRONLY | os.O_CREAT | os.O_EXCL)
            with os.fdopen(fd, 'w') as f:
                f.write(str(os.getpid()))
            return
        except OSError:
            sleep(0.1)

# thread version
def timeout(target, sec):
    from threading import Thread
    from traceback import format_exc
    def pass_return(target, a):
        try:
            a.append(target())
            a.append(0)
        except:
            a.append(format_exc().split('\n')[-2])
            a.append(1)
    a = []
    p = Thread(target=pass_return, args=(target, a))
    p.setDaemon(True)
    p.start()
    p.join(sec)
    if not len(a):
        a.append('Exception: Timeout: custom timeout exceeded (%d seconds)'%(sec, ))
        a.append(2)
    return a[::-1]

# multiprocess version
def timeout(target, sec):
    from multiprocessing import Process, Queue
    from traceback import format_exc
    def pass_return(target, a):
        try:
            a.put(target())
            a.put(0)
        except:
            a.put(format_exc().split('\n')[-2])
            a.put(1)
    a = Queue()
    p = Process(target=pass_return, args=(target, a))
    p.start()
    p.join(sec)
    r = [a.get(), a.get()] if a.qsize() == 2 else ['Exception: Timeout: custom timeout exceeded (%d seconds)'%(sec, ), 2]
    p.terminate()
    return r[::-1]

if __name__ == '__main__':
    pass

'''
exit()
python
'''
