# http://github.com/takeiteasy/esc2esc
#
# MIT License
# 
# Copyright (c) 2025 George Watson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sys import exit, stdin, stdout
from signal import signal, SIGINT
from platform import system
from typing import Optional, Callable

if system() == "Windows":
    import msvcrt
else:
    import termios
    from select import select

def _signal_handler(sig, frame):
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

ESCAPE = 27

def wait2escape(msg: Optional[str] = "Press escape to interrupt...\n",
                key: Optional[int] = ESCAPE,
                handle_signals: Optional[bool] = True,
                signal_handler: Optional[Callable[int, int]] = _signal_handler):
    global __term__
    if not __term__:
        if msg:
            print(msg, end="")
            stdout.flush()
        if handle_signals and signal_handler:
            signal(SIGINT, signal_handler)
        __term__ = Term()
    if kbhit():
        if not key or ord(getch()) == key:
            return False
    return True
