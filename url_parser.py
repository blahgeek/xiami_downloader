#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at May 31 08:09 by BlahGeek@Gmail.com

import sys
if hasattr(sys, 'setdefaultencoding'):
	sys.setdefaultencoding('UTF-8')

from urllib import unquote
def geturl(origin):
	n = int(origin[0])
	origin = origin[1:]
	short_lenth = len(origin) / n
	long_num = len(origin) - short_lenth * n
	l = tuple()
	for i in xrange(0, n):
		length = short_lenth
		if i < long_num:
			length += 1
		l += (origin[0:length], )
		origin = origin[length:]
	ans = ''
	for i in xrange(0, short_lenth + 1):
		for j in xrange(0, n):
			if len(l[j])>i:
				ans += l[j][i]
	return unquote(ans).replace('^', '0')
