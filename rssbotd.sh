#!/bin/bash
Time=540
while true
do
	if ping -c3 www.google.com
		then
		/var/www/cgi-bin/rssbot.py
		wait
	sleep $Time
done
exit 1
