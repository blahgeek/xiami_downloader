#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at May 31 08:37 by BlahGeek@Gmail.com

import sys
if hasattr(sys, 'setdefaultencoding'):
	sys.setdefaultencoding('UTF-8')

from BeautifulSoup import Tag
from url_parser import geturl
import os
import urllib2
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
class track:
	def __init__(self, tag):
		self.id3 = dict()
		for i in ('title', 'album_name', 'artist'):
			self.id3[i] = tag.find(name=i).text
			self.id3[i] = self.id3[i] #.partition(r'<![CDATA[ ')[2]
			self.id3[i] = self.id3[i] #.rpartition(r']]')[0]
		self.url = geturl(tag.find(name='location').text.strip())
		self.picurl = tag.find(name='pic').text.strip()
		self.lyricurl = tag.find(name='lyric').text.strip()
		self._file = self.id3['artist'] + ' - ' + \
				self.id3['title'] + '.' + self.url.rpartition('.')[2]
		sys.stderr.write(self._file + '\n')
	def download(self, path, ReportHook = None):
		self.filename = os.path.join(path, self._file)
		self.lyricfilename = os.path.join(path, 'lyrics', self._file.rpartition('.')[0] + '.lrc')
		if os.path.exists(self.filename):
			sys.stderr.write(' File exists. Ignore.')
			return
		req = urllib2.urlopen(self.url)
		total_size = int(req.info().getheader('Content-Length').strip())
		fout = open(self.filename, 'wb')
		
		read_size = 0
		trunk_size = 10240
		while True:
			_little_data = req.read(trunk_size)
			read_size += len(_little_data)
			if len(_little_data) == 0:
				break
			fout.write(_little_data)
			if ReportHook != None:
				ReportHook(read_size, total_size)
		fout.close()

		easyid3 = EasyID3()
		easyid3['title'] = self.id3['title']
		easyid3['album'] = self.id3['album_name']
		easyid3['artist'] = self.id3['artist']
		easyid3.save(self.filename)

		pic = urllib2.urlopen(self.picurl)
		harid3 = ID3(self.filename)
		harid3.add(APIC(\
				encoding = 3, \
				mime = pic.info().type, \
				type = 3, \
				desc = 'Cover picture from xiami.com fetched by BlahGeek.', \
				data = pic.read()))
		harid3.save()
		sys.stderr.write(' ID3 OK.')

		fout = open(self.lyricfilename, 'wb')
		fout.write(urllib2.urlopen(self.lyricurl).read())
		fout.close()
		sys.stderr.write(' Lyrics OK.')
