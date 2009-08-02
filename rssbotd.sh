#!/bin/bash
Time=540
while true; do
	if ping -c3 www.google.com 2>&1 >/dev/null
		then
		/var/www/cgi-bin/rssbot.py 2>&1 >/dev/null
		wait
	fi
	sleep $Time
done
exit 1
