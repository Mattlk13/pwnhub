#!/bin/bash

for i in range {200..220}
do
	./true-xpl.py $i | ./birds
done
