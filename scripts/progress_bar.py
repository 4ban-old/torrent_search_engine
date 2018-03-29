#from __future__ import print_function
from time import sleep
import sys

mess = "Progress: [%3d]" % 0
sys.stdout.write(mess)
for a in range(101):
    sys.stdout.write("\b\b\b\b")
    sys.stdout.write("\x1b[1;31m%3d\x1b[0m]" % a)
    sys.stdout.flush()

    sleep(0.1)

sys.stdout.write("\b\b\b\b")
sys.stdout.write("\x1b[1;32mOK\x1b[0m]     ")

sys.stdout.flush()

print ''


