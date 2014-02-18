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
\documentclass[ngerman,twocolumn]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[paperwidth=12.5cm,paperheight=10cm,margin=.25cm,top=.5cm]{geometry}
\usepackage{graphicx}
\usepackage{lmodern}
\usepackage{multirow}
\usepackage{rotating}
\usepackage{booktabs}
\usepackage{babel}
\usepackage{textcomp}
\usepackage{tabularx}
\usepackage{supertabular}

\usepackage{xcolor}
\pagecolor{black}
\color{white}
\pagestyle{empty}

\newcolumntype{R}{>{\raggedleft\arraybackslash}X}%
\newcolumntype{L}{>{\raggedright\arraybackslash}X}%
\newcolumntype{C}{>{\centering\arraybackslash}X}%

\setlength{\columnsep}{.5cm}
\setlength{\parindent}{0cm} 

\begin{document}
\sffamily
\flushbottom
 
""")

tex.append(mvglivetex.getTable(stations))

tex.append(r"""

\vspace{1cm}

\rmfamily
\begin{tabularx}{\linewidth}{@{}lR@{}}
\raisebox{.2em}{\large %s} & \multirow{2}{*}{\fontsize{1.2cm}{1em}\selectfont %s} \\
\raisebox{-.2em}{\large %s} \\
\end{tabularx}
\sffamily
\vspace{.5cm}
""" % (time.strftime('%A'), time.strftime('%H:%M'), time.strftime('%x')))

tex.append(mensatex.getTable())

tex.append("")
tex.append(r"\vspace{1em}")

tex.append(whentex.getTex())

tex.append(r"""
\end{document}
""")

with io.open(BASEDIR + '/mvg.tex', 'w', encoding='utf-8') as f:
   f.write('\n'.join(tex))

os.system("pdflatex mvg.tex")
