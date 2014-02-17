#!/usr/bin/python
# -*- coding: UTF-8 -*-

import locale, os, os.path, pygments.lexers, re, subprocess, sys, time, urllib
#locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

URL = 'http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_%Y-%m-%d_421_-de.html' 

if len(sys.argv) == 2:
	wrap = int(sys.argv[1])
else:
	wrap = 40

def fetch(t, tmpdir='/var/tmp'):
	fn = os.path.join(tmpdir, time.strftime('mensa-%Y-%m-%d', t))
	#urllib.urlretrieve(time.strftime(URL, t), fn)[1]
	return open(fn, 'r').read()

def parse(data):
	bucket = []
	active = -1
	lexer = pygments.lexers.get_lexer_for_mimetype('text/html', encoding='utf-8')
	data = data.replace('&amp;', "'n'") #XXX
	for t, v in lexer.get_tokens(data):
		if (str(t) == 'Token.Name.Tag' and v == '<table'):
		        active += 1
		if (str(t) == 'Token.Literal.String' and v == '"menu"'):
		        active += 1
		if (str(t) == 'Token.Name.Tag' and v == '</table>'):
		        active = -1
		if (active <= 0):
		        continue
		if (str(t) != 'Token.Text' or not v.strip() or v.count('\t\t\t') or v in ('fleischlos', 'mit Fleisch', 'PDF', 'vegan')):
			continue
		bucket.append(v)
	return bucket

def format(bucket, wrap=wrap):
    if not bucket: return
    day = bucket[0]
    food = []
    beilagen = []
    aktion = []
    i = 1
    while i < len(bucket):
        if re.match('(?:[TAB]\d+)', bucket[i]):
            food.append((bucket[i], bucket[i+1]))
            i += 2
        if bucket[i] == "Beilagen":
            i += 1
            break
    while i < len(bucket):
        if bucket[i] == "Aktion":
            aktion = map(lambda s: s.strip(), bucket[i+1:])
            break
        else:
            beilagen.append(bucket[i].strip())
            i += 1

    tex = []
    tex.append(r"""

    \begingroup
    \fontsize{8pt}{10pt}\selectfont

    \begin{tabular}{@{}l@{\ }p{4.70cm}@{}}
    \midrule
    """)

    for (v,f) in food:
        tex.append(r" %s & %s \\"%(v,f))

    tex.append(r"""
    \end{tabular}

    \fontsize{6pt}{8pt}\selectfont
    \textbf{Beilagen:} %s\\
    \textbf{Aktion:} %s

    \endgroup
    """%(', '.join(beilagen), ', '.join(aktion)))

    return u'\n'.join(tex)

shorten = lambda s: re.sub(r'([TAB])(?:agesgericht|ktionsessen|iogericht) (\d+)', r'\1\2', s)

def getTable():
    t = time.localtime()
    if t.tm_hour * 60 + t.tm_min > 14 * 60 + 20:
        advance = 1
    else:
        advance = 0

    tex = []

    while True:
        mt = time.localtime(time.time() + advance * 86400)
        output = format(map(shorten, parse(fetch(mt))))
        if output or advance > 30:
            break
        advance += 1

    advance = {0: 'heute', 1: 'morgen'}.get(advance, 'in %d Tagen' % advance)
    tex.append(u"Mensa Arcisstraße %s\\" % advance)

    tex.append(output)

    return '\n'.join(tex)
