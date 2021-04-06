#!/usr/bin/python
#Rafael Gustavo Gassner - 08/2019
#Script to identify the first of the 5 seconds with the most total sync without acks
import sys
import re
from collections import defaultdict
import operator

input_dic={}
output_dic={}

def smtm(input_dic):
    for second in input_dic:
	total_out=0
	count=0
        while count <= 4:
            if str(int(second)+count) in input_dic:
                total_out+=input_dic[str(int(second)+count)]
            count+=1
        output_dic[second]=total_out

def slargest(output_dic):
    for time in output_dic:
	max_second=max(output_dic.iteritems(), key=operator.itemgetter(1))[0]
    print('{} {}'.format(output_dic[max_second],max_second))

for line in sys.stdin:
    search = re.search(' *([0-9]*) ([0-9]*)', line, re.IGNORECASE)
    if search:
        total_sec = search.group(1)
        time = search.group(2)
        input_dic[time] = int(total_sec)

smtm(input_dic)
slargest(output_dic)
