# -*- coding: utf-8 -*-
def print_color(*args, **kwargs):
    '''
    print_color(value, ..., sep=' ', end='\\n', file=sys.stdout, flush=True)

    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    
    Colorizing Windows cmd use ANSI escape code.
    Only supports 0, 1, 30~37, 40~47, 90~97, 100~107
    example: print_color('\\033[1;31mred color\\033[m')
    
    ANSI escape code:
    https://en.wikipedia.org/wiki/ANSI_escape_code
    '''
    
    from sys import platform, stdout
    from locale import getdefaultlocale
    LOCAL = getdefaultlocale()[1] if getdefaultlocale()[1] else 'UTF-8'# for MAC
    
    sep = kwargs['sep'] if 'sep' in kwargs else ' '
    end = kwargs['end'] if 'end' in kwargs else '\n'
    file = kwargs['file'] if 'file' in kwargs else stdout
    flush = kwargs['flush'] if 'flush' in kwargs else True
    
    s = lambda i:(i.encode(LOCAL, errors='replace') if type(i) == type(u'') else i).__str__()
    s = s(sep).join(map(s, args))+s(end)
    
    if platform.startswith('win'):
        
        import re
        from ctypes import windll
        
        GSH = windll.kernel32.GetStdHandle(-11)
        SCTA = windll.kernel32.SetConsoleTextAttribute
        # m = [((i&1)<<2)+(i&2)+((i&4)>>2) for i in range(8)]
        m = [0, 4, 2, 6, 1, 5, 3, 7]
        
        def is_support(s):
            if s == '':
                return True
            try:
                n = int(s)
                return n == 0 or n == 1 or (n >= 30 and n < 38) or (n >= 40 and n < 48) or (n >= 90 and n < 98) or (n >= 100 and n < 108)
            except:
                return False
        
        p = re.compile(r'\033\[[\d\;]*m')
        c = 7
        f = 0
        SCTA(GSH, 7)
        for i in p.finditer(s):
            a = i.span()
            if f != a[0]:
                file.write(s[f:a[0]])
                if flush:
                    file.flush()
            ca = map(lambda i:0 if i == '' else int(i), filter(is_support, s[a[0]+2:a[1]-1].split(';')))
            for j in ca:
                if j == 0:
                    c = 7
                elif j == 1:
                    c |= 8
                elif j >= 30 and j < 38:
                    c = c&248|m[j%10]
                elif j >= 40 and j < 48:
                    c = c&15|(m[j%10]<<4)
                elif j >= 90 and j < 98:
                    c = c&240|m[j%10]|8
                elif j >= 100 and j < 108:
                    c = c&15|(m[j%10]<<4)|128
            SCTA(GSH, c)
            f = a[1]
        file.write(s[f:])
        if flush:
            file.flush()
        SCTA(GSH, 7)
    
    else:
        file.write(s)
        if flush:
            file.flush()

if __name__ == '__main__':
    map(lambda l:map(lambda k:print_color('\n'+'\n'.join(map(lambda j:'\033[%dm'%j+'\t'.join(map(lambda i:'\033[%dm%d %d'%(i, i, j), range(k, k+8)))+'\033[0m', range(l, l+8)))), [30, 90]), [40, 100])
    print
    #from itertools import product
    #a = ['0', '1', '31', '91']
    #map(lambda i:print_color('\033[%sm%s\033[m'%(i, i)), map(lambda i:';'.join(i), product(a, a, a, a)))
    #print
