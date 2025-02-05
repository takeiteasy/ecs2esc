from esc2esc import wait2escape
from time import sleep
from sys import stdout, exit

def test_signal(_: int, __: int):
    print("goodbye!")
    exit(0)

while wait2escape(msg="Hello.",
                  signal_handler=test_signal):
    sleep(0.1)
    print(".", end="")
    stdout.flush()

