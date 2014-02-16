#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import io
import os
import MVGLive

stations = {
        'Pinakotheken': [27, 28, 100],
        'Türkenstraße': [154],
        'Universität': [3, 6]}

BASEDIR = os.path.dirname(os.path.realpath(__file__))

alldepartures = {}
for (station,lines) in stations.iteritems():
    departures = {}
    data = MVGLive.getlivedata(station,20)
    for departure in data:
        line = int(departure['linename'].replace('U',''))
        if not line in lines:
            continue
        k = (line, departure['product'],
                departure['destination'].replace('Forschungszentrum',
                'Forschungsz.'))
        l = departures.get(k, [])
        if (len(l) >= 3):
            continue
        l.append(departure['time'])
        departures[k] = l
    alldepartures[station] = departures

# collapse Tram to Sendlinger Tor
alldepartures['Pinakotheken'][0, 'Tram', 'Sendlinger Tor'] = sorted(
    alldepartures['Pinakotheken'][27, 'Tram', 'Sendlinger Tor'] +
    alldepartures['Pinakotheken'][28, 'Tram', 'Sendlinger Tor'])
del alldepartures['Pinakotheken'][27, 'Tram', 'Sendlinger Tor']
del alldepartures['Pinakotheken'][28, 'Tram', 'Sendlinger Tor']

tex = u'''
\\documentclass[varwidth=true,border=10pt]{standalone}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{graphicx}
\\usepackage{lmodern}
\\pagestyle{empty}

\\usepackage{xcolor}
\\pagecolor{black}
\\color{white}

\\begin{document}
\\sffamily
'''

for station,departures in alldepartures.items():
    tex += station.decode('utf-8')
    tex += '''

\\begin{tabular}{l@{\\ }c@{\\ }p{3.3cm}@{\\ }r}
\\rlap{Linie} & \\hphantom{555} & Ziel & \\hphantom{55,\\,55,\\,55}\\llap{Abfahrt in Min.}\\\\
\\hline
\\rule{0pt}{1.1em}%
'''
    for (line,prod,dest),v in sorted(departures.items()):
        tex += "\\includegraphics[height=.8em]{" + prod + ".pdf} & "
        if line == 0:
            tex += " & "
        elif line <= 8:
            tex += "\\includegraphics[height=.8em]{U%i.pdf} & "%line
        else:
            tex += "%i & "%line
        tex += (u" & ".join((dest,
            ',\\,'.join(map(lambda s : "\\hphantom{55}\\llap{%s}"%s, sorted(v)[:3]))))
                + "\\\\\n")
    tex += '''
\\end{tabular}

        '''

tex += """
\\end{document}
"""

with io.open(BASEDIR + '/mvg.tex', 'w', encoding='utf-8') as f:
    f.write(tex)
