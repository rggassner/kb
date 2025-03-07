#!/bin/bash
cd /opt/categorization/
wget https://github.com/olbat/ut1-blacklists/raw/master/blacklists/adult/domains.gz
gzip -d domains.gz
echo "{">/opt/categorization/suspect.json
for domain in `cat /opt/categorization/domains`
do 
	echo "\"$domain\": \"YES\",">>/opt/categorization/suspect.json
done
echo "}">>/opt/categorization/suspect.json
