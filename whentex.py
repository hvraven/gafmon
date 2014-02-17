#/usr/bin/env python2
# -*- coding: UTF-8 -*-

from subprocess import Popen,PIPE
import datetime, locale

def getDates():
    output = Popen(["when", "--past=0", "--future=60", "--noheader", "--wrap=0"],
            stdout=PIPE).communicate()[0]
    output = map(lambda s: s.split(), output.strip().split('\n'))
    l = locale.getlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, 'C')
    v = map(lambda l: (datetime.datetime.strptime(' '.join(l[1:4]),
        '%Y %b %d'), ' '.join(l[4:])), output)
    locale.setlocale(locale.LC_ALL, l)
    return v


def getTex():
    tex = []

    tex.append(ur"\begin{tabular}{@{}r@{\ }l@{}}")

    dates = getDates()

    for (date,text) in dates[:5]:
        if date <= datetime.datetime.today():
            cake = ur"\includegraphics[height=1em]{Cake.png}"
        else:
            cake = ""

        tex.append(ur"%s & %s %s\\"%(date.strftime('%e.%m.'),text,cake))

    tex.append(r"\end{tabular}")

    return u'\n'.join(tex)
