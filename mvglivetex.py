#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from collections import defaultdict
import MVGLive

shortdest = {
        (u'154', u'Bus',    u'Bruno-Walter-Ring'): (u'154',u'Arabellapark', u'B'),
        (u'28',  u'Tram',   u'Sendlinger Tou'):    (u'27', u'Sendlinger Tou', u''),
        (u'U2',  u'U-Bahn', u'Harthof'):           (u'U2', u'Feldmoching', u'H'),
        (u'U2',  u'U-Bahn', u'Milbertshofen'):     (u'U2', u'Feldmoching', u'M'),
        (u'U2',  u'U-Bahn', u'Innsbrucker Ring'):  (u'U2', u'Messestadt Ost', u'I'),
        (u'U2',  u'U-Bahn', u'Kolumbusplatz'):     (u'U2', u'Messestadt Ost', u'K'),
        (u'U2',  u'U-Bahn', u'Sendlinger Tou'):    (u'U2', u'Messestadt Ost', u'S'),
        (u'U3',  u'U-Bahn', u'Sendlinger Tou'):    (u'U3', u'Fürstenried West', u'S'),
        (u'U3',  u'U-Bahn', u'Thalkirchen'):       (u'U3', u'Fürstenried West', u'T'),
        (u'U3',  u'U-Bahn', u'Olympiazentrum'):    (u'U3', u'Moosach', u'O'),
        (u'U3',  u'U-Bahn', u'Münchner Freiheit'): (u'U3', u'Moosach', u'F'),
        (u'U6',  u'U-Bahn', u'Alte Heide'):        (u'U6', u'Fröttmaning', u'A'),
        (u'U6',  u'U-Bahn', u'Kieferngarten'):     (u'U6', u'Fröttmaning', u'K'),
        (u'U6',  u'U-Bahn', u'Ditlindenstraße'):   (u'U6', u'Fröttmaning', u'D'),
        (u'U6',  u'U-Bahn', u'Garching-Forschungszentrum'): (u'U6', u'Garching-FoZe.', u''),
        (u'U6',  u'U-Bahn', u'Harras'):            (u'U6', u'Klinikum Großhadern', u'h'),
        (u'U6',  u'U-Bahn', u'Implerstraße'):      (u'U6', u'Klinikum Großhadern', u'I'),
        (u'U6',  u'U-Bahn', u'Münchner Freiheit'): (u'U6', u'Fröttmaning', u'F'),
        }

def getTable(stations):
    alldepartures = {}
    for (station,lines) in stations.iteritems():
        departures = defaultdict(list)
        data = MVGLive.getlivedata(station,30)
        for departure in data:
            line = departure['linename'].decode('utf-8')
            if not line in lines:
                continue
            k = ( line, departure['product'], departure['destination'])
            l = departures.get(k, [])
            l.append((int(departure['time']), r''))
            departures[k] = l
        alldepartures[station] = departures

    # rename and collapse some destinations
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
    tex.append(ur"""
    \begin{tabular}{@{\ }l@{\ }c@{\ }p{3.2cm}@{\ }r@{\ }}
    \rlap{Linie} & \hphantom{555} & Ziel & \hphantom{55,\,55,\,55}\llap{Abfahrten}\\
    """)

    for station, departures in alldepartures.iteritems():
        tex.append(ur"\midrule")

        for (line,prod,dest),v in sorted(departures.iteritems(), 
                key=lambda ((s,_,y),x) : int(s.replace('U', ''))):
            tex.append(ur"""\includegraphics[height=.8em]{%s.pdf} & """ % prod)
            if int(line.replace('U','')) <= 8:
                tex.append(ur"\includegraphics[height=.8em]{%s.pdf} & " % line)
            else:
                tex.append("%s & " % line)
            tex.append(ur"%s & %s \\" % (
                    dest,
                    r",\,".join(map(lambda (t,sup) : 
                        r"\hphantom{55}\llap{%i}" % t + (sup and
                            r"\rlap{\textsuperscript{\tiny{%s}}}" % sup),
                        sorted(v)[:3]))
                    ))

    tex.append(ur"\midrule")

    if usedshorts:
        tex.append(ur"\multicolumn{4}{l}{\parbox{5.5cm}{\tiny{Abkürzungen: ")
        for short,dest in usedshorts.iteritems():
            if short:
                tex.append(ur"%s: %s " % (short , dest))
        tex.append("}}}\n")

    tex.append(ur"""\end{tabular}
    """)
    return u'\n'.join(tex)
