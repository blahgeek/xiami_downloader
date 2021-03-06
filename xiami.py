#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2014-04-19

import os
import sys
import tempfile
import shutil
from BeautifulSoup import BeautifulStoneSoup
from rex import rex
from urlparse import urlparse
from argparse import ArgumentParser
from lib.http import download
from lib.progress import ProgressBar
from lib.track import Track


def parse_url(url):
    url = urlparse(url)
    assert url.netloc == 'www.xiami.com', 'Must be a xiami.com url.'
    m = (rex(r'//song/showcollect/id/(\d+)/') == url.path)
    if bool(m):
        return 'collect', m[1]
    m = (rex(r'//(\w+)/(\d+)/') == url.path)
    assert bool(m), 'Url path not valid.'
    return m[1], m[2]


def get_xml_url(typ, number):
    url = r'http://www.xiami.com/song/playlist/id/' + str(number)
    if typ == 'album':
        url += '/type/1'
    elif typ == 'artist':
        url += '/type/2'
    elif typ == 'collect':
        url += '/type/3'
    return url


def get_tracks(xml_url):
    xml_f, _ = download(xml_url)
    soup = BeautifulStoneSoup(xml_f.read())
    return soup.findAll(name='track')


def main():
    parser = ArgumentParser(description=
        'Download a single track, collection, album, artist from xiami.com '
        'with lyric and ID3 infomation filled')
    parser.add_argument('URL', 
        help='Xiami url to download, can be song/artist/album/collect')
    parser.add_argument('-d', '--destination', default='~/Music/iTunes/iTunes Media/Automatically Add to iTunes.localized/',
        help='Save path, default to ~/Music/iTunes/iTunes Media/Automatically Add to iTunes.localized/')
    parser.add_argument('-l', '--lyric-destination',
        help='Lyric saving path, do not download lyric if not specified')
    args = parser.parse_args()

    tempdir = tempfile.gettempdir()
    destination = os.path.expanduser(args.destination)

    xml_url = get_xml_url(*parse_url(args.URL))
    tracks = get_tracks(xml_url)
    print >> sys.stderr, len(tracks), 'track(s) found.'

    for x in tracks:
        progress_bar = ProgressBar()
        track = Track(x)
        filename = track.download(tempdir, progress_bar)
        if args.lyric_destination:
            track.download_lyric(args.lyric_destination, progress_bar)
        track.patch_id3(tempdir, progress_bar)
        shutil.move(os.path.join(tempdir, filename),
                    os.path.join(destination, filename))


if __name__ == '__main__':
    main()
