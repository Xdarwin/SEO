#!/bin/sh
echo 'Installing pdfminer library'
pip install pdfminer.six

echo 'Processing the files'
echo 'Command line tool:'
echo 'write [word] : get suggestions about [word]'
echo 'quit : quit the program'
echo 'Waiting for the proccessing of files to finish'
python run.py ricou/internet_chap1.pdf ricou/internet_chap2.pdf -n 2 -r 5
