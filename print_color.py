# -*- coding: utf-8 -*-
# window platform
# support number: 0, 1, 30~37, 40~47, 90~97, 100~107

def print_color(s, end='\n'):
    
    from sys import platform, stdout
    
    if platform.startswith('win'):
        
        import re, ctypes
        
        GSH = ctypes.windll.kernel32.GetStdHandle(-11)
        SCTA = ctypes.windll.kernel32.SetConsoleTextAttribute
        m = {0:0, 1:4, 2:2, 3:6, 4:1, 5:5, 6:3, 7:7}
        
        def is_support(s):
            try:
                n = int(s)
                return n == 0 or n == 1 or (n >= 30 and n < 38) or (n >= 40 and n < 48) or (n >= 90 and n < 98) or (n >= 100 and n < 108)
            except:
                return False
        
        p = re.compile(r'\033\[[\d\;]*m')
        c = [0, 7]
        f = 0
        SCTA(GSH, 7)
        for i in p.finditer(s):
            a = i.span()
            if f != a[0]:
                stdout.write(s[f:a[0]])
                stdout.flush()
            ca = map(int, filter(is_support, s[a[0]+2:a[1]-1].split(';')))
            si = []
            for j in ca:
                if j == 0 or j == 1:
                    si.append(j)
                else:
                    c[j//10%2] = m[j%10]+(0 if j < 90 else 8)
            if ca == [] or ca == [0]:
                SCTA(GSH, 7)
            else:
                c[1] += 0 if not len(si) else 8 if si[-1] == 1 and c[1] < 8 else -8 if si[-1] == 0 and c[1] >= 8 else 0
                SCTA(GSH, (c[0]<<4)+c[1])
            f = a[1]
        stdout.write(s[f:]+end)
        stdout.flush()
        SCTA(GSH, 7)
    
    else:
        stdout.write(s+end)
        stdout.flush()

if __name__ == '__main__':
    map(lambda l:map(lambda k:print_color('\n'+'\n'.join(map(lambda j:'\033[%dm'%j+'\t'.join(map(lambda i:'\033[%dm%d %d'%(i, i, j), range(k, k+8)))+'\033[0m', range(l, l+8)))), [30, 90]), [40, 100])
    print
    #print_color('\033[37;41masdf\033[m')
