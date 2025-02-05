from sys import exit, stdin
from signal import signal, SIGINT
from platform import system
from typing import Optional

if system() == "Windows":
    import msvcrt
else:
    import termios
    from select import select

def signal_handler(sig, frame):
    exit(0)

def _getch():
    return stdin.read(1)

def _wgetch():
    return msvcrt.getch().decode('utf-8')

def _kbhit():
    r, _, _ = select([stdin], [], [], 0)
    return r is not None and r != []

if system() == "Windows":
    getch = _wgetch
    kbhit = msvcrt.kbhit
else:
    getch = _getch
    kbhit = _kbhit

class Term:
    def __init__(self):
        self.fd = stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
    
    def __del__(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

__term__ = None

def wait2escape(msg: Optional[str] = "Press escape to interrupt...\n",
                key: Optional[int] = 27):
    global __term__
    if not __term__:
        if msg:
            print(msg, end="")
        signal(SIGINT, signal_handler)
        __term__ = Term()
    if kbhit():
        if not key or ord(getch()) == 27:
            return False
    return True
