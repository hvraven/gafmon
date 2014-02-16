#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import io, os, time
from collections import defaultdict
import MVGLive

stations = {
        'Pinakotheken': ['27', '28', '100'],
        'Türkenstraße': ['154'],
        'Universität': ['U3', 'U6']}

BASEDIR = os.path.dirname(os.path.realpath(__file__))

alldepartures = {}
for (station,lines) in stations.iteritems():
    departures = defaultdict(list)
    data = MVGLive.getlivedata(station,30)
    for departure in data:
        line = departure['linename']
        if not line in lines:
            continue
        k = (
		line, 
		departure['product'],
                departure['destination'])
        l = departures.get(k, [])
        l.append((int(departure['time']), ''))
        departures[k] = l
    alldepartures[station] = departures

# collapse Tram to Sendlinger Tor
if ('28', 'Tram', 'Sendlinger Tor') in alldepartures['Pinakotheken']:
    i = alldepartures['Pinakotheken'].get(('27', 'Tram', 'Sendlinger Tor'), [])
    if i:
        del alldepartures['Pinakotheken']['27', 'Tram', 'Sendlinger Tor']
    i += alldepartures['Pinakotheken']['28', 'Tram', 'Sendlinger Tor']
    del alldepartures['Pinakotheken']['28', 'Tram', 'Sendlinger Tor']
    alldepartures['Pinakotheken']['', 'Tram', 'Sendlinger Tor'] = sorted(i)

# rename and collapse some destinations
shortdest = {
        ('U6',  'U-Bahn', 'Garching-Forschungszentrum'): ('Garching-FoZe.', ''),
        ('U6',  'U-Bahn', 'Alte Heide'):                 ('Fröttmaning', 'A'),
        ('U6',  'U-Bahn', 'Münchner Freiheit'):          ('Fröttmaning', 'F'),
        ('U6',  'U-Bahn', 'Hadern'):                     ('Klinikum Großhadern', 'H'),
        ('154', 'Bus',    'Bruno-Walter-Ring'):          ('Arabellapark', 'B'),
        }

usedshorts = []
for departures in alldepartures.itervalues():
    for ((line,prod,olddest),(newdest,short)) in shortdest.iteritems():
        i = departures.get((line,prod,olddest), [])
        if i:
            departures[line,prod,newdest] += map(lambda (t,_):
                    (t,short), i)
            del departures[line,prod,olddest]
            if short:
                usedshorts.append((short,olddest))

tex = []
tex.append(r"""
\documentclass[aspectratio=54,9pt]{beamer}
%%\usetheme{boxes}
\usetheme{Frankfurt}
\usecolortheme{beetle}
\usetheme{Dresden}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{lmodern}

\usepackage{xcolor}
%%\pagecolor{black}
%%\color{white}
%%\setbeamercolor{background canvas}{bg=}
%%\setbeamercolor{palette primary}{fg=green}
%%\setbeamercovered{transparent}

\setbeamertemplate{navigation symbols}{}

\begin{document}
\sffamily
 
\begin{frame}
\frametitle{%s}
""" % time.ctime())

for station, departures in alldepartures.iteritems():
    tex.append(r"""
\begin{tabular}{l@{\ }c@{\ }p{3cm}@{\ }r}
\multicolumn{4}{c}{%s} \\
\rlap{Linie} & \hphantom{555} & Ziel & \hphantom{55,\,55,\,55}\llap{Abfahrt}\\
\hline
\rule{0pt}{1.1em}%%
""" % station.decode('utf-8'))

    for (line,prod,dest),v in sorted(departures.iteritems(), 
            key=lambda ((s,_,y),x) : int(s.replace('U', ''))):
        tex.append(r"""\includegraphics[height=.8em]{%s.pdf} & """ % prod)
        if int(line.replace('U','')) <= 8:
            tex.append(r"\includegraphics[height=.8em]{%s.pdf} & " % line)
        else:
            tex.append("%s & " % line)
        tex.append(r"%s & %s \\" % (
		dest,
		r",\,".join(map(lambda (t,sup) : 
                    r"\hphantom{55}\llap{%i}" % t + (sup and
                        r"\rlap{\textsuperscript{\tiny{%s}}}" % sup),
                    sorted(v)[:3]))
		))
    tex.append(r"\end{tabular} \\")

if usedshorts:
    tex.append(u"\\tiny{Abkürzungen: ")
    for short,dest in usedshorts:
        if short:
            tex.append(r"%s: %s " % (short , dest.decode('utf-8')))
    tex.append("}\n")

tex.append(r"""%s\\
\end{frame}
\end{document}
""")

with io.open(BASEDIR + '/mvg.tex', 'w', encoding='utf-8') as f:
   f.write('\n'.join(tex))


