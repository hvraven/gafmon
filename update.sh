#!/bin/zsh

pushd /home/gaf/gafmon
./gafmon.py && kill -HUP $(< ~/.gafmon.pid)
popd
