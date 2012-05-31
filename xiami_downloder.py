#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at May 31 10:28 by BlahGeek@Gmail.com

import sys
if hasattr(sys, 'setdefaultencoding'):
	sys.setdefaultencoding('UTF-8')

from track import track
from BeautifulSoup import *
import urllib2

baseurl = r'http://www.xiami.com/song/playlist/id/'
albumurl_root = r'/type/1'
artisturl_root = r'/type/2'

def progress_bar(current, total):
	sys.stderr.write(str(current) + ' of ' + str(total)\
			+ ' Bytes downloaded.\r')

if __name__ == '__main__':
	if len(sys.argv) != 3 or sys.argv[1] not in ['song', 'album', 'artist']:
		print 'usage: ' + argv[0] + ' song|album|artist ID\n'
		sys.exit(-1)
	url = baseurl + sys.argv[2]
	if sys.argv[1] == 'album':
		url += albumurl_root
	if sys.argv[1] == 'artist':
		url += artisturl_root
	
	raw_data = urllib2.urlopen(url).read()
	tracks = BeautifulStoneSoup(raw_data).findAll(name='track')
	for i in tracks:
		song = track(i)
		song.download('./', ReportHook = progress_bar)
		sys.stderr.write('\n\n')
