#!/bin/bash
i="diancan"
pid=`ps auxf | grep $i | grep -v "grep" | awk {'print $2'}`
echo $pid;
sudo kill $pid;
sleep 1s
python diancan.py --port=9000 1>log 2>&1 &
