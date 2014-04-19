#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2014-04-18

import os
from os.path import splitext
from urlparse import urlparse
import requests
from StringIO import StringIO

sess = requests.Session()
sess.headers.update({
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
    })

CHUNK_SIZE = 40960


def download(url, save_path=None, filename='', progress_bar=None):
    ''' @url: url to download, unicode
        @save_path: save file here, return file-like object if None
        @progress_bar: show progress '''
    req = sess.get(url, stream=True)
    if save_path is None:
        return StringIO(req.content), req.headers.get('Content-Type', '')
    _, ext = splitext(urlparse(url).path.split('/')[-1])
    assert ext, 'File extension must not be empty'
    filename = splitext(filename)[0] + ext
    filepath = os.path.join(save_path, filename).encode('utf8')
    size = int(req.headers.get('Content-Length', '-1').strip())
    downloaded = 0
    if progress_bar is not None:
        progress_bar.set_filename(filename)
    try:
        with open(filepath, 'wb') as f:
            for chunk in req.iter_content(CHUNK_SIZE):
                f.write(chunk)
                downloaded += CHUNK_SIZE
                if progress_bar is None:
                    continue
                progress_bar.update(downloaded, size)
    except KeyboardInterrupt:
        os.remove(filepath)
        if progress_bar is not None:
            progress_bar.msg('\nInterrupt, file removed.\n')
        raise
    else:
        if progress_bar is not None:
            progress_bar.finish()
        return filename
