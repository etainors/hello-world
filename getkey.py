try:
    from msvcrt import getch

    def getkey():
        r = getch()
        if r == '\x00' or r == '\xe0':
            r += getch()
        return r

except ImportError:

    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def getkey():
        import signal
        def handler(signum, frame):
            raise Exception
        signal.signal(signal.SIGALRM, handler)
        r = getch()
        try:
            while True:
                signal.setitimer(signal.ITIMER_REAL, 0.000001)
                r += getch()
        except:
            return r
