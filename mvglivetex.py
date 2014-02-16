#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import io, os, time
from collections import defaultdict
import MVGLive

stations = {
        'Pinakotheken': ['27', '28', '100'],
        'Schellingstraße': ['154'],
        'Universität': ['U3', 'U6'],
        'Theresienstraße': ['U2', 'U8'],
        'Odeonsplatz': ['U5']}

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

# rename and collapse some destinations
shortdest = {
        ('154', 'Bus',    'Bruno-Walter-Ring'): ('154', 'Arabellapark', 'B'),
        ('28',  'Tram',   'Sendlinger Tor'):    ('27', 'Sendlinger Tor', ''),
        ('U2',  'U-Bahn', 'Harthof'):           ('U2', 'Feldmoching', 'H'),
        ('U2',  'U-Bahn', 'Milbertshofen'):     ('U2', 'Feldmoching', 'M'),
        ('U2',  'U-Bahn', 'Innsbrucker Ring'):  ('U2', 'Messestadt Ost', 'I'),
        ('U2',  'U-Bahn', 'Kolumbusplatz'):     ('U2', 'Messestadt Ost', 'K'),
        ('U2',  'U-Bahn', 'Sendlinger Tor'):    ('U2', 'Messestadt Ost', 'S'),
        ('U3',  'U-Bahn', 'Sendlinger Tor'):    ('U3', 'Fürstenried West', 'S'),
        ('U3',  'U-Bahn', 'Thalkirchen'):       ('U3', 'Fürstenried West', 'T'),
        ('U3',  'U-Bahn', 'Olympiazentrum'):    ('U3', 'Moosach', 'O'),
        ('U3',  'U-Bahn', 'Münchner Freiheit'): ('U3', 'Moosach', 'F'),
        ('U6',  'U-Bahn', 'Alte Heide'):        ('U6', 'Fröttmaning', 'A'),
        ('U6',  'U-Bahn', 'Kieferngarten'):     ('U6', 'Fröttmaning', 'K'),
        ('U6',  'U-Bahn', 'Ditlindenstraße'):   ('U6', 'Fröttmaning', 'D'),
        ('U6',  'U-Bahn', 'Garching-Forschungszentrum'): ('U6', 'Garching-FoZe.', ''),
        ('U6',  'U-Bahn', 'Harras'):            ('U6', 'Klinikum Großhadern', 'h'),
        ('U6',  'U-Bahn', 'Implerstraße'):      ('U6', 'Klinikum Großhadern', 'I'),
        ('U6',  'U-Bahn', 'Münchner Freiheit'): ('U6', 'Fröttmaning', 'F'),
        }

usedshorts = {}
for departures in alldepartures.itervalues():
    for ((oldline,prod,olddest),(newline,newdest,short)) in shortdest.iteritems():
        i = departures.get((oldline,prod,olddest), [])
        if i:
            departures[newline,prod,newdest] += map(lambda (t,_):
                    (t,short), i)
            del departures[oldline,prod,olddest]
            if short:
                usedshorts[short] = olddest

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
\usepackage{multirow}
\usepackage{rotating}
\usepackage{booktabs}

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

\begin{tabular}{l@{\ }c@{\ }p{3cm}@{\ }r}
\rlap{Linie} & \hphantom{555} & Ziel & \hphantom{55,\,55,\,55}\llap{Abfahrten}\\
""" % time.ctime())

for station, departures in alldepartures.iteritems():
#    tex.append(r" \multicolumn{4}{l}{%s} \\ " % station.decode('utf-8'))
    tex.append(r"\midrule")

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

tex.append(r"\midrule")

if usedshorts:
    tex.append(u"\\multicolumn{4}{l}{\\tiny{Abkürzungen: ")
    for short,dest in usedshorts.iteritems():
        if short:
            tex.append(r"%s: %s " % (short , dest.decode('utf-8')))
    tex.append("}}\n")

tex.append(r"""\end{tabular}
\end{frame}
\end{document}
""")

with io.open(BASEDIR + '/mvg.tex', 'w', encoding='utf-8') as f:
   f.write('\n'.join(tex))
