#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2014-04-19

import os
import sys
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
    parser.add_argument('-n', '--no-lyric', action='store_true',
        help='Do not download lyric')
    parser.add_argument('-d', '--destination', default='.',
        help='Save path, default to current directory')
    parser.add_argument('-l', '--lyric-destination', default='./lyric/',
        help='Lyric save path')
    args = parser.parse_args()

    for path in (args.destination, args.lyric_destination):
        if not os.path.exists(path):
            print >> sys.stderr, 'mkdir', path
            os.mkdir(path)
    xml_url = get_xml_url(*parse_url(args.URL))
    tracks = get_tracks(xml_url)
    print >> sys.stderr, len(tracks), 'track(s) found.'

    for x in tracks:
        progress_bar = ProgressBar()
        track = Track(x)
        track.download(args.destination, progress_bar)
        if not args.no_lyric:
            track.download_lyric(args.lyric_destination, progress_bar)
        track.patch_id3(progress_bar)


if __name__ == '__main__':
    main()
