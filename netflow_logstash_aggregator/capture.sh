#!/bin/bash
#Rafael Gustavo Gassner - 17/05/2019
#Configure expiring time for nfcapd and
#launches one capture deamon for each sender
#Updated 10/2019 with feature to forward netflow based on senders.dat information
base_dir=/opt/netflow
senders=`cat $base_dir/senders.dat`
mkdir $base_dir/flows

for process in `ps -ef f | grep nfcap | grep -v grep | awk {'print $2'}`
do
	kill $process
done

for i in $senders
do
        fw=`echo $i | cut -d , -f 1`
        port=`echo $i | cut -d , -f 2`
        fhost=`echo $i | cut -d , -f 3`
        fport=`echo $i | cut -d , -f 4`
        mkdir $base_dir/flows/$fw
        #-e expire
        #-w align rotation
        #-D daemon mode
        #-l base dir
        #-p port
        #-x execute
	#-R forward
        nfexpire -t 1H -u $base_dir/flows/$fw
        forward=""
        if [[ -n "$fhost" ]]
        then
                forward="-R $fhost/$fport"
        fi
        nfcapd -e -w -D -l $base_dir/flows/$fw -p $port -x "$base_dir/dump.sh $fw" `echo $forward`
done
