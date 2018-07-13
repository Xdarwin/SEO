#!/bin/sh

echo 'Processing the files'
echo 'Command line tool:'
echo 'write [word] : get suggestions about [word]'
echo 'quit : quit the program'
python run.py ricou/internet_chap1.pdf ricou/internet_chap2.pdf -n 2 -r 5
