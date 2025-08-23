#!/bin/bash
base_dir="/opt/netflow/dic"
curl -vs https://check.torproject.org/exit-addresses 2>&1 | grep ExitAdd | cut -d" " -f2 | awk '{ print "\""$1"\": \"YES\"" '} > $base_dir/torexil.yml
