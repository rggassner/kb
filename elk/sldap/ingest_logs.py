#!/bin/bash
cd ../logs
for file in `ls -1 *.gz`
do
        gzip -d $file &
done
wait
cd ../ldap-access-log-humanizer
for file in `ls -1 ../logs`
do
        echo $file
        ./humanizer.py --input_file ../logs/$file --output_file_name ../humanized/$file && cat ../humanized/$file | nc -q 1 127.0.0.1 5003 &
done
wait
rm ../logs/* -rf
