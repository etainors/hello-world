# -*- coding: utf-8 -*-
# window platform
# support number: 0, 1, 30~37, 40~47, 90~97, 100~107
# https://en.wikipedia.org/wiki/ANSI_escape_code
from sys import stdout as _stdout
from sys import platform as _platform
_is_win = _platform.startswith('win')

if _is_win:
    import ctypes as _ctypes
    _GSH = _ctypes.windll.kernel32.GetStdHandle(-11)
    _SCTA = _ctypes.windll.kernel32.SetConsoleTextAttribute
    _m = {0:0, 1:4, 2:2, 3:6, 4:1, 5:5, 6:3, 7:7}

    import re as _re
    _p = _re.compile(r'\033\[[\d\;]*m')

    def _is_support(s):
        try:
            n = int(s)
            return n == 0 or n == 1 or (n >= 30 and n < 38) or (n >= 40 and n < 48) or (n >= 90 and n < 98) or (n >= 100 and n < 108)
        except:
            return False

def print_color(s, end='\n'):

    if _is_win:

        c = 7
        f = 0
        _SCTA(_GSH, 7)
        for i in _p.finditer(s):
            a = i.span()
            if f != a[0]:
                _stdout.write(s[f:a[0]])
                _stdout.flush()
            ca = map(int, filter(_is_support, s[a[0]+2:a[1]-1].split(';')))
            for j in ca:
                if j == 0:
                    c = 7
                elif j == 1:
                    c |= 8
                elif j >= 30 and j < 38:
                    c = c&248|_m[j%10]
                elif j >= 40 and j < 48:
                    c = c&15|(_m[j%10]<<4)
                elif j >= 90 and j < 98:
                    c = c&240|_m[j%10]|8
                elif j >= 100 and j < 108:
                    c = c&15|(_m[j%10]<<4)|128
            _SCTA(_GSH, c)
            f = a[1]
        _stdout.write(s[f:]+end)
        _stdout.flush()
        _SCTA(_GSH, 7)

    else:
        _stdout.write(s+end)
        _stdout.flush()

if __name__ == '__main__':
    map(lambda l:map(lambda k:print_color('\n'+'\n'.join(map(lambda j:'\033[%dm'%j+'\t'.join(map(lambda i:'\033[%dm%d %d'%(i, i, j), range(k, k+8)))+'\033[0m', range(l, l+8)))), [30, 90]), [40, 100])
    print
