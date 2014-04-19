#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2014-04-18

from .decrypt import decrypt
from .http import download
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

class Track(object):
    ''' A song '''

    def __init__(self, tag):
        ''' @tag: a BeautifulSoup Tag representing a track'''
        keys = ('title', 'album_name', 'artist')
        values = map(lambda x: tag.find(name=x).text, keys)
        self.id3 = dict(zip(keys, values))
        geturl = lambda key: tag.find(name=key).text.strip()
        self.url = decrypt(geturl('location'))
        self.picurl = geturl('pic')
        self.lyricurl = geturl('lyric')
        if not self.lyricurl.endswith('.lrc'):
            self.lyricurl = None
        self.filename = self.id3['artist'] + ' - ' + self.id3['title']
        self.filename_with_ext = self.filename + '.mp3'

    def download(self, save_path, progress_bar):
        self.filename_with_ext = download(self.url, save_path, 
                                          self.filename, progress_bar)
        return self.filename_with_ext

    def download_lyric(self, save_path, progress_bar):
        if self.lyricurl is None:
            progress_bar.msg('No lyric available.\n')
            return
        progress_bar.msg('Downloading lyric...')
        download(self.lyricurl, save_path, self.filename, None)
        progress_bar.msg('Done.\n')

    def patch_id3(self, progress_bar):
        progress_bar.msg('Patching ID3...')
        cover_f, mime_type = download(self.picurl)
        easyid3 = EasyID3()
        easyid3['title'] = self.id3['title']
        easyid3['album'] = self.id3['album_name']
        easyid3['artist'] = self.id3['artist'].split(';')
        easyid3['performer'] = easyid3['artist'][0]
        easyid3.save(self.filename_with_ext)

        harid3 = ID3(self.filename_with_ext)
        harid3.add(APIC(
                encoding = 3,
                mime = mime_type,
                type = 3,
                desc = 'Cover picture from xiami.com fetched by BlahGeek.',
                data = cover_f.read()))
        harid3.save()
        progress_bar.msg('Done.\n')
