try:
    from msvcrt import getch

    def getkey():
        r = getch()
        if r == '\x00' or r == '\xe0':
            r += getch()
        return r

    _is_win = True

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
                signal.setitimer(signal.ITIMER_REAL, 0.001)
                r += getch()
        except:
            return r

    _is_win = False

def keyselect(s, a):
    if len(a) == 1:
        return a[0]
    a.append('\x03')# Ctrl+c
    print s,
    r = getkey()
    while r not in a:
        r = getkey()
    if r == '\x03':
        raise KeyboardInterrupt
    print r
    return r

class keymap:
    '''
    mapping key and getkey value:
    
    only    key : .{key}
    Shift + key : .S_{key}
    Ctrl  + key : .C_{key}
    Alt   + key : .A_{key}
    
    key name below:
    
    special: .ESC
             .BKSP
             .TAB
             .ENTER
             .SPACE
             .F1 ~ .F12
             .HOME
             .UP
             .PGUP
             .LEFT
             .RIGHT
             .END
             .DOWN
             .PGDN
             .INS
             .DEL
    number: ._0 ~ ._9
    symbol: .DASH      -
            .EQUAL     =
            .LSB       [
            .RSB       ]
            .SEMICOLON ;
            .QUOTE     \'
            .GA        `
            .BACKSLASH \\
            .COMMA     ,
            .DOT       .
            .SLASH     /
    letter: .a ~ .z
    '''
    def __init__(self):
        # https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
        # scancode 00 is normally an error code
        # scancode 01 Esc
        self.ESC = '\x1b'
        self.S_ESC = '\x1b'
        self.C_ESC = '\x1b'
        self.A_ESC = '\x01'
        # scancode 02 1!
        self._1 = '1'
        self.S_1 = '!'
        self.C_1 = None
        self.A_1 = '1' if _is_win else '\x1b1'
        # scancode 03 2@
        self._2 = '2'
        self.S_2 = '@'
        self.C_2 = '\x00\x03' if _is_win else '\x00'
        self.A_2 = '2' if _is_win else '\x1b2'
        # scancode 04 3#
        self._3 = '3'
        self.S_3 = '#'
        self.C_3 = None if _is_win else '\x1b'
        self.A_3 = '3' if _is_win else '\x1b3'
        # scancode 05 4$
        self._4 = '4'
        self.S_4 = '$'
        self.C_4 = None if _is_win else '\x1c'
        self.A_4 = '4' if _is_win else '\x1b4'
        # scancode 06 5%
        self._5 = '5'
        self.S_5 = '%'
        self.C_5 = None if _is_win else '\x1d'
        self.A_5 = '5' if _is_win else '\x1b5'
        # scancode 07 6^
        self._6 = '6'
        self.S_6 = '^'
        self.C_6 = None if _is_win else '\x1e'
        self.A_6 = '6' if _is_win else '\x1b6'
        # scancode 08 7&
        self._7 = '7'
        self.S_7 = '&'
        self.C_7 = None if _is_win else '\x1f'
        self.A_7 = '7' if _is_win else '\x1b7'
        # scancode 09 8*
        self._8 = '8'
        self.S_8 = '*'
        self.C_8 = None if _is_win else '\x7f'
        self.A_8 = '8' if _is_win else '\x1b8'
        # scancode 0A 9(
        self._9 = '9'
        self.S_9 = '('
        self.C_9 = None
        self.A_9 = '9' if _is_win else '\x1b9'
        # scancode 0B 0)
        self._0 = '0'
        self.S_0 = ')'
        self.C_0 = None
        self.A_0 = '0' if _is_win else '\x1b0'
        # scancode 0C -_ (dash)
        self.DASH = '-'
        self.S_DASH = '_'
        self.C_DASH = None if _is_win else '\x1f'
        self.A_DASH = '-' if _is_win else '\x1b-'
        # scancode 0D =+ (equal)
        self.EQUAL = '='
        self.S_EQUAL = '+'
        self.C_EQUAL = None
        self.A_EQUAL = '=' if _is_win else '\x1b='
        # scancode 0E BKSP
        self.BKSP = '\x08' if _is_win else '\x7f'
        self.S_BKSP = '\x08'
        self.C_BKSP = '\x7f'
        self.A_BKSP = '\x08' if _is_win else '\x1b\x7f'
        # scancode 0F TAB
        self.TAB = '\t'
        self.S_TAB = '\t' if _is_win else '\x1b[Z'
        self.C_TAB = '\x00\x94' if _is_win else None
        self.A_TAB = None
        # scancode 10 q
        self.q = 'q'
        self.S_q = 'Q'
        self.C_q = '\x11'
        self.A_q = 'q' if _is_win else '\x1bq'
        # scancode 11 w
        self.w = 'w'
        self.S_w = 'W'
        self.C_w = '\x17'
        self.A_w = 'w' if _is_win else '\x1bw'
        # scancode 12 e
        self.e = 'e'
        self.S_e = 'E'
        self.C_e = '\x05'
        self.A_e = 'e' if _is_win else '\x1be'
        # scancode 13 r
        self.r = 'r'
        self.S_r = 'R'
        self.C_r = '\x12'
        self.A_r = 'r' if _is_win else '\x1br'
        # scancode 14 t
        self.t = 't'
        self.S_t = 'T'
        self.C_t = '\x14'
        self.A_t = 't' if _is_win else '\x1bt'
        # scancode 15 y
        self.y = 'y'
        self.S_y = 'Y'
        self.C_y = '\x19'
        self.A_y = 'y' if _is_win else '\x1by'
        # scancode 16 u
        self.u = 'u'
        self.S_u = 'U'
        self.C_u = '\x15'
        self.A_u = 'u' if _is_win else '\x1bu'
        # scancode 17 i
        self.i = 'i'
        self.S_i = 'I'
        self.C_i = '\t'
        self.A_i = 'i' if _is_win else '\x1bi'
        # scancode 18 o
        self.o = 'o'
        self.S_o = 'O'
        self.C_o = '\x0f'
        self.A_o = 'o' if _is_win else '\x1bo'
        # scancode 19 p
        self.p = 'p'
        self.S_p = 'P'
        self.C_p = '\x10'
        self.A_p = 'p' if _is_win else '\x1bp'
        # scancode 1A [{ (left square bracket)
        self.LSB = '['
        self.S_LSB = '{'
        self.C_LSB = '\x1b'
        self.A_LSB = '[' if _is_win else '\x1b['
        # scancode 1B ]} (right square bracket)
        self.RSB = ']'
        self.S_RSB = '}'
        self.C_RSB = '\x1d'
        self.A_RSB = ']' if _is_win else '\x1b]'
        # scancode 1C ENTER
        self.ENTER = '\r'
        self.S_ENTER = '\r'
        self.C_ENTER = '\n' if _is_win else '\r'
        self.A_ENTER = None if _is_win else '\x1b\r'
        # scancode 1D CTRL
        # scancode 1E a
        self.a = 'a'
        self.S_a = 'A'
        self.C_a = '\x01'
        self.A_a = 'a' if _is_win else '\x1ba'
        # scancode 1F s
        self.s = 's'
        self.S_s = 'S'
        self.C_s = '\x13'
        self.A_s = 's' if _is_win else '\x1bs'
        # scancode 20 d
        self.d = 'd'
        self.S_d = 'D'
        self.C_d = '\x04'
        self.A_d = 'd' if _is_win else '\x1bd'
        # scancode 21 f
        self.f = 'f'
        self.S_f = 'F'
        self.C_f = '\x06'
        self.A_f = 'f' if _is_win else '\x1bf'
        # scancode 22 g
        self.g = 'g'
        self.S_g = 'G'
        self.C_g = '\x07'
        self.A_g = 'g' if _is_win else '\x1bg'
        # scancode 23 h
        self.h = 'h'
        self.S_h = 'H'
        self.C_h = '\x08'
        self.A_h = 'h' if _is_win else '\x1bh'
        # scancode 24 j
        self.j = 'j'
        self.S_j = 'J'
        self.C_j = '\n'
        self.A_j = 'j' if _is_win else '\x1bj'
        # scancode 25 k
        self.k = 'k'
        self.S_k = 'K'
        self.C_k = '\x0b'
        self.A_k = 'k' if _is_win else '\x1bk'
        # scancode 26 l
        self.l = 'l'
        self.S_l = 'L'
        self.C_l = '\x0c'
        self.A_l = 'l' if _is_win else '\x1bl'
        # scancode 27 ;:
        self.SEMICOLON = ';'
        self.S_SEMICOLON = ':'
        self.C_SEMICOLON = None
        self.A_SEMICOLON = ';' if _is_win else '\x1b;'
        # scancode 28 '"
        self.QUOTE = "'"
        self.S_QUOTE = '"'
        self.C_QUOTE = None
        self.A_QUOTE = "'" if _is_win else "\x1b'"
        # scancode 29 `~ (grave accent)
        self.GA = '`'
        self.S_GA = '~'
        self.C_GA = None
        self.A_GA = '`' if _is_win else '\x1b`'
        # scancode 2A L Shift
        # scancode 2B \| (backslash)
        self.BACKSLASH = '\\'
        self.S_BACKSLASH = '|'
        self.C_BACKSLASH = '\x1c'
        self.A_BACKSLASH = '\\' if _is_win else '\x1b\\'
        # scancode 2C z
        self.z = 'z'
        self.S_z = 'Z'
        self.C_z = '\x1a'
        self.A_z = 'z' if _is_win else '\x1bz'
        # scancode 2D x
        self.x = 'x'
        self.S_x = 'X'
        self.C_x = '\x18'
        self.A_x = 'x' if _is_win else '\x1bx'
        # scancode 2E c
        self.c = 'c'
        self.S_c = 'C'
        self.C_c = '\x03'
        self.A_c = 'c' if _is_win else '\x1bc'
        # scancode 2F v
        self.v = 'v'
        self.S_v = 'V'
        self.C_v = '\x16'
        self.A_v = 'v' if _is_win else '\x1bv'
        # scancode 30 b
        self.b = 'b'
        self.S_b = 'B'
        self.C_b = '\x02'
        self.A_b = 'b' if _is_win else '\x1bb'
        # scancode 31 n
        self.n = 'n'
        self.S_n = 'N'
        self.C_n = '\x0e'
        self.A_n = 'n' if _is_win else '\x1bn'
        # scancode 32 m
        self.m = 'm'
        self.S_m = 'M'
        self.C_m = '\r'
        self.A_m = 'm' if _is_win else '\x1bm'
        # scancode 33 ,< (comma)
        self.COMMA = ','
        self.S_COMMA = '<'
        self.C_COMMA = None
        self.A_COMMA = ',' if _is_win else '\x1b,'
        # scancode 34 .> (dot)
        self.DOT = '.'
        self.S_DOT = '>'
        self.C_DOT = None
        self.A_DOT = '.' if _is_win else '\x1b.'
        # scancode 35 /? (slash)
        self.SLASH = '/'
        self.S_SLASH = '?'
        self.C_SLASH = '\x1f'
        self.A_SLASH = '/' if _is_win else '\x1b/'
        # scancode 36 R SHIFT
        # scancode 37 (Keypad *) or (*/PrtScn) on a 83/84-key keyboard
        # scancode 38 ALT
        # scancode 39 SPACE
        self.SPACE = ' '
        self.S_SPACE = ' '
        self.C_SPACE = ' '
        self.A_SPACE = ' ' if _is_win else '\x1b '
        # scancode 3A CapsLock
        # scancode 3B F1
        self.F1 = '\x00;' if _is_win else '\x1b[11~'
        self.S_F1 = '\x00T' if _is_win else '\x1b[23~'
        self.C_F1 = '\x00^' if _is_win else '\x1b[11~'
        self.A_F1 = '\x00h' if _is_win else '\x1b\x1b[11~'
        # scancode 3C F2
        self.F2 = '\x00<' if _is_win else '\x1b[12~'
        self.S_F2 = '\x00U' if _is_win else '\x1b[24~'
        self.C_F2 = '\x00_' if _is_win else '\x1b[12~'
        self.A_F2 = '\x00i' if _is_win else '\x1b\x1b[12~'
        # scancode 3D F3
        self.F3 = '\x00=' if _is_win else '\x1b[13~'
        self.S_F3 = '\x00V' if _is_win else '\x1b[25~'
        self.C_F3 = '\x00`' if _is_win else '\x1b[13~'
        self.A_F3 = '\x00j' if _is_win else '\x1b\x1b[13~'
        # scancode 3E F4
        self.F4 = '\x00>' if _is_win else '\x1b[14~'
        self.S_F4 = '\x00W' if _is_win else '\x1b[26~'
        self.C_F4 = '\x00a' if _is_win else '\x1b[14~'
        self.A_F4 = '\x00k' if _is_win else '\x1b\x1b[14~'
        # scancode 3F F5
        self.F5 = '\x00?' if _is_win else '\x1b[15~'
        self.S_F5 = '\x00X' if _is_win else '\x1b[28~'
        self.C_F5 = '\x00b' if _is_win else '\x1b[15~'
        self.A_F5 = '\x00l' if _is_win else '\x1b\x1b[15~'
        # scancode 40 F6
        self.F6 = '\x00@' if _is_win else '\x1b[17~'
        self.S_F6 = '\x00Y' if _is_win else '\x1b[29~'
        self.C_F6 = '\x00c' if _is_win else '\x1b[17~'
        self.A_F6 = '\x00m' if _is_win else '\x1b\x1b[17~'
        # scancode 41 F7
        self.F7 = '\x00A' if _is_win else '\x1b[18~'
        self.S_F7 = '\x00Z' if _is_win else '\x1b[31~'
        self.C_F7 = '\x00d' if _is_win else '\x1b[18~'
        self.A_F7 = '\x00n' if _is_win else '\x1b\x1b[18~'
        # scancode 42 F8
        self.F8 = '\x00B' if _is_win else '\x1b[19~'
        self.S_F8 = '\x00[' if _is_win else '\x1b[32~'
        self.C_F8 = '\x00e' if _is_win else '\x1b[19~'
        self.A_F8 = '\x00o' if _is_win else '\x1b\x1b[19~'
        # scancode 43 F9
        self.F9 = '\x00C' if _is_win else '\x1b[20~'
        self.S_F9 = '\x00\\' if _is_win else '\x1b[33~'
        self.C_F9 = '\x00f' if _is_win else '\x1b[20~'
        self.A_F9 = '\x00p' if _is_win else '\x1b\x1b[20~'
        # scancode 44 F10
        self.F10 = '\x00D' if _is_win else '\x1b[21~'
        self.S_F10 = '\x00]' if _is_win else '\x1b[34~'
        self.C_F10 = '\x00g' if _is_win else '\x1b[21~'
        self.A_F10 = '\x00q' if _is_win else '\x1b\x1b[21~'
        # scancode 45 F11
        self.F11 = '\xe0\x85' if _is_win else '\x1b[23~'
        self.S_F11 = '\xe0\x87' if _is_win else '\x1b[23~'
        self.C_F11 = '\xe0\x89' if _is_win else '\x1b[23~'
        self.A_F11 = '\xe0\x8b' if _is_win else '\x1b\x1b[23~'
        # scancode 46 F12
        self.F12 = '\xe0\x86' if _is_win else '\x1b[24~'
        self.S_F12 = '\xe0\x88' if _is_win else '\x1b[24~'
        self.C_F12 = '\xe0\x8a' if _is_win else '\x1b[24~'
        self.A_F12 = '\xe0\x8c' if _is_win else '\x1b\x1b[24~'
        # scancode 47 HOME
        self.HOME = '\xe0G' if _is_win else '\x1b[1~'
        self.S_HOME = '\xe0G' if _is_win else '\x1b[1~'
        self.C_HOME = '\xe0w' if _is_win else None
        self.A_HOME = '\x00\x97' if _is_win else '\x1b\x1b[1~'
        # scancode 48 UP
        self.UP = '\xe0H' if _is_win else '\x1b[A'
        self.S_UP = '\xe0H' if _is_win else '\x1b[A'
        self.C_UP = '\xe0\x8d' if _is_win else '\x1b[A'
        self.A_UP = '\x00\x98' if _is_win else '\x1b\x1b[A'
        # scancode 49 PGUP
        self.PGUP = '\xe0I' if _is_win else '\x1b[5~'
        self.S_PGUP = '\xe0I' if _is_win else '\x1b[5~'
        self.C_PGUP = '\xe0\x86' if _is_win else '\x1b[5~'
        self.A_PGUP = '\x00\x99' if _is_win else '\x1b\x1b[5~'
        # scancode 4A (Keypad -)
        # scancode 4B LEFT
        self.LEFT = '\xe0K' if _is_win else '\x1b[D'
        self.S_LEFT = '\xe0K' if _is_win else '\x1b[D'
        self.C_LEFT = '\xe0s' if _is_win else '\x1b[D'
        self.A_LEFT = '\x00\x9b' if _is_win else '\x1b\x1b[D'
        # scancode 4C (Keypad 5)
        # scancode 4D RIGHT
        self.RIGHT = '\xe0M' if _is_win else '\x1b[C'
        self.S_RIGHT = '\xe0M' if _is_win else '\x1b[C'
        self.C_RIGHT = '\xe0t' if _is_win else '\x1b[C'
        self.A_RIGHT = '\x00\x9d' if _is_win else '\x1b\x1b[C'
        # scancode 4E (Keypad +)
        # scancode 4F END
        self.END = '\xe0O' if _is_win else '\x1b[4~'
        self.S_END = '\xe0O' if _is_win else '\x1b[4~'
        self.C_END = '\xe0u' if _is_win else '\x1b[4~'
        self.A_END = '\x00\x9f' if _is_win else '\x1b\x1b[4~'
        # scancode 50 DOWN
        self.DOWN = '\xe0P' if _is_win else '\x1b[B'
        self.S_DOWN = '\xe0P' if _is_win else '\x1b[B'
        self.C_DOWN = '\xe0\x91' if _is_win else '\x1b[B'
        self.A_DOWN = '\x00\xa0' if _is_win else '\x1b\x1b[B'
        # scancode 51 PGDN
        self.PGDN = '\xe0Q' if _is_win else '\x1b[6~'
        self.S_PGDN = '\xe0Q' if _is_win else '\x1b[6~'
        self.C_PGDN = '\xe0v' if _is_win else '\x1b[6~'
        self.A_PGDN = '\x00\xa1' if _is_win else '\x1b\x1b[6~'
        # scancode 52 INS
        self.INS = '\xe0R' if _is_win else '\x1b[2~'
        self.S_INS = '\xe0R' if _is_win else 'INS'
        self.C_INS = '\xe0\x92' if _is_win else None
        self.A_INS = '\x00\xa2' if _is_win else '\x1b\x1b[2~'
        # scancode 53 DEL
        self.DEL = '\xe0S' if _is_win else '\x1b[3~'
        self.S_DEL = '\xe0S' if _is_win else '\x1b[3~'
        self.C_DEL = '\xe0\x93' if _is_win else None
        self.A_DEL = '\x00\xa3' if _is_win else '\x1b\x1b[3~'

if __name__ == '__main__':
    print repr(getkey())
