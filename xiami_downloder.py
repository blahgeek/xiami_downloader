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
download_types = ['song', 'album', 'artist', 'collect']

from time import time
class progress_bar:
	def __init__(self):
		self.lastTime = time()
		self.lastSize = 0
		self.bar_size = 30
		self.speed = 0
	def __call__(self, current, total):
		done_length = int(float(current) / float(total) * self.bar_size)
		print >> sys.stderr, '\r[' + '='*done_length + ' '*(self.bar_size-done_length) + ']  ', 
		print >> sys.stderr, '%3d%%  %d kB/s  ' % \
				(100 * current / total, self.speed), 
		nowTime = time()
		if nowTime - self.lastTime > 0.5:
			self.speed = (current - self.lastSize) / ((nowTime - self.lastTime) * 1024)
			self.lastTime = nowTime
			self.lastSize = current

if __name__ == '__main__':
	if len(sys.argv) < 3 or sys.argv[1] not in download_types:
		print 'usage:', sys.argv[0], '|'.join(download_types), 'ID [path]\n'
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
	sys.stderr.write(str(len(tracks)) + ' song(s) found.\n\n')
	for i in tracks:
		song = track(i)
		song.download(save_path, ReportHook = progress_bar())
		sys.stderr.write('\n\n')
