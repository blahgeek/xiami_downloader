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

import re
if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] not in download_types:
        print 'usage:', sys.argv[0], '|'.join(download_types), 'ID [path]\n'
        sys.exit(-1)
    _find = re.findall(r'\d+$', sys.argv[2])
    if len(_find) == 0:
        print 'invalid ID'
        sys.exit(-1)
    url = baseurl + _find[0]
    if sys.argv[1] == 'album':
        url += albumurl_root
    if sys.argv[1] == 'artist':
        url += artisturl_root
    if sys.argv[1] == 'collect':
        url += collecturl_root
    if len(sys.argv) >= 4:
        save_path = sys.argv[3]
    
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.70 Safari/537.17')
    raw_data = urllib2.urlopen(req).read()
    tracks = BeautifulStoneSoup(raw_data).findAll(name='track')
    sys.stderr.write(str(len(tracks)) + ' song(s) found.\n\n')
    for i in tracks:
        song = track(i)
        song.download(save_path, ReportHook = progress_bar())
        sys.stderr.write('\n\n')
