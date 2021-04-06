#!/bin/bash
#Script to process aggregations and filters against the
#netflow capture files, and to package data to logstash
#Rafael Gustavo Gassner - 05/2019
IFS=$'\n'
base_dir=/opt/netflow
aggs=`cat $base_dir/aggregations.dat`
filters=`cat $base_dir/filters.dat` 
orderby=`cat $base_dir/orderby.dat`
fw=$1
top=50
for file in `ls $base_dir/flows/$fw/ -1 --sort time -r | grep -P "nfcapd\.[0-9]{12}"`
do
        for i in $aggs
        do
                agg_name=`echo $i | tr "," "-"`
		for filter in $filters
		do
			for order in $orderby
			do
				filter_name=`echo $filter | cut -d , -f 1`
				filter_content=`echo $filter | cut -d , -f 2-`
                		nfdump -N -r $base_dir/flows/$fw/$file  -o "fmt:start=%tsr,duration=%td,src=%sa,dst=%da,packets=%pkt,bytes=%byt,pps=%pps,bps=%bps,bpp=%bpp,flows=%fl,sport=%sp,dport=%dp,proto=%pr,inif=%in,outif=%out,firewall=$fw,agg=$agg_name,filter=$filter_name,order=$order" -O $order -n $top -q -A $i -a "$filter_content" | netcat -q 1  localhost 9000
			done
		done
        done
        #For every interface
        for inif in `nfdump -N -r $base_dir/flows/$fw/$file  -o "fmt:inif=%in" -q -A inif | awk {'print $2'}`
        do
                result=`nfdump -N -r $base_dir/flows/$fw/$file  -o "fmt:flag=%flg,start=%tsr" -q -a "IN IF $inif" | grep -P "flag=...\...S." | cut -d , -f 2 | cut -d = -f 2 | cut -d \. -f 1 | sort | uniq -c | $base_dir/top5Interval.py`
                acklessSyn=`echo $result | awk {'print $1'}`
                start=`echo $result | awk {'print $2'}`
                if [[ "$start" -ne "" ]]
                then
                        if [[ "$acklessSyn" -ne "" ]]
                        then
                                echo "start=$start.000,acklessSyn=$acklessSyn,inif=$inif,firewall=$fw,agg=acklessSyn,filter=all" | netcat -q 1  localhost 9000
                        fi
                fi
        done
        rm $base_dir/flows/$fw/$file
done
