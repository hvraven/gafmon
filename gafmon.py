#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import io, os, time, locale
import mvglivetex, mensatex, whentex
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

stations = {
        'Pinakotheken': ['27', '28', '100'],
        'Schellingstraße': ['154'],
        'Universität': ['U3', 'U6'],
        'Theresienstraße': ['U2', 'U8'],
        'Odeonsplatz': ['U5']}

BASEDIR = os.path.dirname(os.path.realpath(__file__))

tex = []
tex.append(r"""
\documentclass[ngerman]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[paperwidth=12.5cm,paperheight=10cm,margin=.5cm]{geometry}
\usepackage{graphicx}
\usepackage{lmodern}
\usepackage{multirow}
\usepackage{rotating}
\usepackage{booktabs}
\usepackage{babel}


\usepackage{xcolor}
\pagecolor{black}
\color{white}
\pagestyle{empty}

\begin{document}
\sffamily
 
\noindent
\begin{minipage}{.5\linewidth}
""")

tex.append(mvglivetex.getTable(stations))

tex.append(r"""
\end{minipage}
\quad
\begin{minipage}{.46\linewidth}
%s
\vspace{1cm}
""" % time.strftime('%x %X'))

tex.append(mensatex.getTable())

tex.append("")
tex.append(r"\vspace{1em}")

tex.append(whentex.getTex())

tex.append(r"""
\end{minipage}
\end{document}
""")

with io.open(BASEDIR + '/mvg.tex', 'w', encoding='utf-8') as f:
   f.write('\n'.join(tex))

os.system("pdflatex mvg.tex")
os.system("mudraw -w 1280 -o mvg.png mvg.pdf")
