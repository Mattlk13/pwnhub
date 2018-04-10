#!/bin/sh

socat TCP4-LISTEN:1337,reuseaddr,fork EXEC:"./birds" 1>&2 &

