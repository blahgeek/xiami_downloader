#!/usr/bin/env python2
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
collecturl_root = r'/type/3'
save_path = '/home/blahgeek/Music/'

def progress_bar(current, total):
	bar_size = 30
	done_length = int(float(current) / float(total) * bar_size)
	sys.stderr.write('\r[' + '='*done_length + ' '*(bar_size-done_length) + ']  ' + \
			str(current) + ' of ' + str(total) + ' Bytes downloaded.')

if __name__ == '__main__':
	if len(sys.argv) < 3 or sys.argv[1] not in ['song', 'album', 'artist', 'collect']:
		print 'usage: ' + sys.argv[0] + ' song|album|artist ID [path]\n'
		sys.exit(-1)
	url = baseurl + sys.argv[2]
	if sys.argv[1] == 'album':
		url += albumurl_root
	if sys.argv[1] == 'artist':
		url += artisturl_root
	if sys.argv[1] == 'collect':
		url += collecturl_root
	if len(sys.argv) >= 4:
		save_path = sys.argv[3]
	
	raw_data = urllib2.urlopen(url).read()
	tracks = BeautifulStoneSoup(raw_data).findAll(name='track')
	for i in tracks:
		song = track(i)
		song.download(save_path, ReportHook = progress_bar)
		sys.stderr.write('\n\n')
