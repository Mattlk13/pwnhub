#!/usr/bin/python
from pwn import *

host = ''
port =

def exploit (r):


if __name__ == '__main__':
	e = ELF ('./binary')
	libc = ELF ('./libc.so')

	if len (sys.argv) > 1:
		r = remote (host, port)
		exploit (r)
	else:
		r = process ('./binary', env = {'LD_PRELOAD' : './libc.so'})
		pause ()
		exploit (r)
