#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2014-04-18

import sys
from time import time

class ProgressBar(object):
    ''' Simple progress bar in console. '''

    BAR_WIDTH = 30

    def __init__(self):
        self.last_time = time()
        self.last_downloaded = 0
        self.speed = 0
        self.size = -1

    def update(self, downloaded, size):
        self.size = size
        width = int(float(downloaded) / float(size) * self.BAR_WIDTH)
        print >> sys.stderr, '\r[' + '=' * width + ' ' * (self.BAR_WIDTH - width) + ']',
        print >> sys.stderr, '%3d%% %d kB/s' % (100*downloaded/size, self.speed),
        now = time()
        if now - self.last_time < 0.5:
            return
        self.speed = (downloaded - self.last_downloaded) / ((now - self.last_time) * 1024)
        self.last_time = now
        self.last_downloaded = downloaded

    def set_filename(self, filename):
        print >> sys.stderr, filename.encode('utf8')

    def finish(self):
        self.update(self.size, self.size)
        print >> sys.stderr, '\n',

    def msg(self, msg):
        print >> sys.stderr, msg.encode('utf8'),
