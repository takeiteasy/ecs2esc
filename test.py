from esc2esc import wait2escape
from time import sleep
from sys import stdout

while wait2escape(msg="Hello."):
    sleep(0.1)
    print(".", end="")
    stdout.flush()

