#!/usr/bin/python3
import ijson
import bz2,shutil,os,subprocess
from glob import glob
from pathlib import Path
from collections import Counter
import time
input_directory='input'
tmp_directory='tmp'
output_directory='output'
packet_count='0'
compression_buffer=1000000

def xtract(compressed_file,file_name):
    print('Extracting {}'.format(compressed_file))
    with bz2.BZ2File(compressed_file) as fr, open(tmp_directory+'/'+file_name+'.out','wb') as fw:
        shutil.copyfileobj(fr,fw,length = compression_buffer)

def pflog2json(file_name):
    with open(tmp_directory+'/'+file_name+'.json', "w") as outfile:
        if packet_count == '0':
            subprocess.run(['tshark','-nV','-r', tmp_directory+'/'+file_name+'.out','-T','json'],stdout=outfile)
        else:
            subprocess.run(['tshark','-nV','-c'+packet_count,'-r', tmp_directory+'/'+file_name+'.out','-T','json'],stdout=outfile)

def ingest(file_name,c):
    with open(tmp_directory+'/'+file_name+'.json', "rb") as f:
        for record in ijson.items(f,'item'):
            src=record['_source']['layers']['ip']['ip.src']
            dst=record['_source']['layers']['ip']['ip.dst']
            proto=''
            if 'udp' in record['_source']['layers']:
                dport=record['_source']['layers']['udp']['udp.dstport']
                proto='udp'
            elif 'tcp' in record['_source']['layers']:
                dport=record['_source']['layers']['tcp']['tcp.dstport']
                proto='tcp'
            elif 'icmp' in record['_source']['layers']:
                dport=record['_source']['layers']['icmp']['icmp.type']
                proto='icmp'
            elif 'igmp' in record['_source']['layers']:
                dport=record['_source']['layers']['igmp']['igmp.version']
                proto='igmp'
            elif record['_source']['layers']['frame']['frame.protocols'] == 'pflog:ip:data':
                dport='pflog'
                proto='pflog'
            else:
                print(record)
                quit()
            c[(src,dst,proto,dport)]+=1

def dumpf(c):
    with open(output_directory+'/'+str(time.time()), 'w') as f:
        for k,v in  c.most_common():
            f.write( "{} {}\n".format(k,v) )

c=Counter()
for compressed_file in glob(input_directory+'/**/*.gz', recursive=True):
    file_name=Path(os.path.basename(compressed_file)).stem
    xtract(compressed_file,file_name)
    pflog2json(file_name)
    ingest(file_name,c)
    print(c)
    dumpf(c)
    os.remove(tmp_directory+'/'+file_name+'.out')
    os.remove(tmp_directory+'/'+file_name+'.json')
