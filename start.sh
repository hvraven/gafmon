#!/bin/sh

pushd /home/gaf/gafmon
./gafmon.py
mupdf mvg.pdf&
echo $! > ~/.gafmon.pid
sleep 1
xdotool search --classname mupdf windowmove 0 0 key f key W
popd
