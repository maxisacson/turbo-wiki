#!/usr/bin/python
# coding=UTF-8

import urllib
import urllib2
from random import *
import time
from bs4 import BeautifulSoup
import curses
import locale
import datetime
import re

locale.setlocale(locale.LC_ALL,'')

def wiki(window):
	eng = 4497604.
	swe = 1616898.
	norm = eng + swe
	swe_w = swe/norm;

	cont = r"^(div|span)$"
	this_breaks = r"^(Other_projects|References|See_also|catlinks|Further_reading|External_links)$"
	this_skips = r"^(Other_projects|References|Referenser|K\.C3\.A4llor|Externa_l\.C3\.A4nkar|Se_\.C3\.A4ven|See_also|catlinks|Further_reading|External_links|External_websites|toc|toctitle)$"

	while True:
		window.clear()
		x = random()
		if x <= swe_w:
			lang = "sv"
		elif x > swe_w and x <= norm:
			lang = "en"

		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#		resource = opener.open(	\
#			"http://en.wikipedia.org/wiki/Mihail_Vântu")
		resource = opener.open("http://" + lang + ".wikipedia.org/wiki/Special:Random")
		data = resource.read()
		resource.close()
		soup = BeautifulSoup(data)
		[h, w] = window.getmaxyx()
		maxrows = float(h)

		try:
			output = soup.title.get_text() + "\n" + (w/2)*"-" + "\n"
			if ('Inga underarter finns listade' in soup.get_text() or 'may refer to' in soup.get_text() \
				or 'kan syfta på' in soup.get_text()):
				continue
			window.addstr(0,0,output.encode("utf-8"), curses.A_BOLD);
			pars = soup.find('div', id="mw-content-text").find_all(\
				['p','h2','h3', 'h4', 'h5', 'li'])
			for s in pars:
				if s:
					s = BeautifulSoup(str(s))
					if s.find_all(id=re.compile(this_skips)):
						break
					elif s.find('h2') \
						and not s.find('span', id=re.compile(this_skips)) \
						and not s.find('div', id=re.compile(this_skips)) \
						and not s.find(text=re.compile(\
						r"^(Inneh.ll|Contents)$"\
						)):
							output = "\n-- "+s.get_text()+" --"
							output = re.sub(\
								r"\[(edit|redigera\ \|\ redigera\ wikitext)\]","",output)
							window.addstr(output.encode("utf-8"), curses.A_BOLD)
					elif s.find('h3') \
						and not s.find('span', id=re.compile(this_skips)) \
						and not s.find('div', id=re.compile(this_skips)):
							output = "\n"+s.get_text()
							output = re.sub(r"\[edit\]","",output)
							window.addstr(output.encode("utf-8"), curses.A_BOLD)
					elif s.find('p'):
						output = "\n"+s.get_text()+"\n"
						window.addstr(output.encode("utf-8"))
					elif s.find('li') \
						and not s.find('li', id=re.compile(r"^(cite)"))\
						and not s.find('li', attrs={"class": "external text"})\
						and not s.find('li', attrs={"class": re.compile(r"^(toc)")})\
						and not re.compile(r"^(v|t|e)$").search(s.li.get_text()):
							output = "\n\t** "+s.li.get_text()
							window.addstr(output.encode("utf-8"))
					else:
						continue
			[ypos, xpos] = window.getyx()
			#window.addstr(str(ypos) + ":" + str(xpos))
			rows = float(ypos)
			weight = rows/maxrows
			r = random()
			if r <= weight:
				pass
			else:
				continue

			window.refresh()
			m = datetime.datetime.now().minute
			s = datetime.datetime.now().second
			switch_at = 60*60
			c = (switch_at - m*60 - s)
			time.sleep(c)
		except curses.error:
			pass

curses.initscr()
curses.curs_set(0)
curses.start_color()
curses.wrapper(wiki)
