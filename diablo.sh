#!/bin/bash
sleep 2
export DISPLAY=:0 
xdotool key z
xdotool key x
xdotool key c
xdotool key v
now=`date +%s%N`
z=$now
zInterval="10300000000"
x=$now
xInterval="617000000000"
c=$now
cInterval="9040000000"
v=$now
vInterval="14400000000"
#leftB=$now
#leftBInterval="100000000"
while (test 1)
do
	now=`date +%s%N`
	if (test $(($now-$z)) -gt $zInterval)
	then
		xdotool key z
		z=$now
	fi
	if (test $(($now-$x)) -gt $xInterval)
	then
		xdotool key x
		x=$now
	fi
	if (test $(($now-$c)) -gt $cInterval)
	then
		xdotool key c
		c=$now
	fi
	if (test $(($now-$v)) -gt $vInterval)
	then
		xdotool key v
		v=$now
	fi
	#if (test $(($now-$leftB)) -gt $leftBInterval)
	#then
		#xdotool keydown shift click 1 keyup shift
	#	xdotool click 3
	#	leftB=$now
	#fi
	sleep .1
done
