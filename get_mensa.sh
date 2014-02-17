#!/bin/zsh

OUTDIR=/var/tmp

for d ({01..28}) ; do
  DATE=$(date --date="+$d day" +%F)
  wget -O "$OUTDIR/mensa-$DATE" "http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_${DATE}_421_-de.html"
done
