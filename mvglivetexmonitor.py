#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import io
import os
import json
import MVGLive

stations = []
stations.append('Pinakotheken')
stations.append('Türkenstraße')
stations.append('Universität')
#stations.append('Maxvorstadt')

BASEDIR = os.path.dirname(os.path.realpath(__file__))

alldepartures = []
departures = []
for station in stations:
  alldepartures.append(MVGLive.getlivedata(station))


collected = 0
currentdeparture = 0
while collected < 9:
  for departureset in alldepartures:
    for departure in departureset:
      if departure['time'] == currentdeparture:
        departures.append(departure)
        collected += 1
  currentdeparture += 1

# rewrite symbols
for departure in departures:
  departure['productsymbol'] = departure['productsymbol'].replace('.gif', '.pdf')

tex = '''
\\documentclass[varwidth=true,border=2pt]{standalone}
\\pagestyle{empty}
\\usepackage[T1]{fontenc}
\\usepackage{lmodern}
\\usepackage{graphicx}

\\usepackage{xcolor}
\\pagecolor{black}
\\color{white}

%\\usepackage{fontspec}
%\\setmainfont{cmss}

\\usepackage{datetime}

\\begin{document}
\\sffamily
\\begin{tabular}{c@{\ }lp{4.5cm}r}
\\multicolumn{2}{l}{Linie} & Ziel & \\llap{Abfahrt in Min.}\\\\
\\hline
\\rule{0pt}{1.1em}%
'''

for departure in departures:
    tex += ("\\includegraphics[width=.85em]{" + departure['productsymbol'] + "} & " +
            departure['linename'] + " & " +
            departure['destination'] + " & " + 
            str(departure['time']) + "\\\\\n")

tex += """
\\end{tabular}

\\tiny{Updated: \currenttime}
\\end{document}
"""

with io.open(BASEDIR + '/mvg.tex', 'w', encoding='utf-8') as f:
    f.write(tex)
