#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-06-20

# Dropzone Action Info
# Name: Xiami Downloader
# Description: Xiami.com music downloader
# Handles: Text
# Creator: BlahGeek
# URL: http://blog.blahgeek.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# OptionsNIB: ChooseFolder
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.5

import xiami
import tempfile
import shutil
from lib import progress
import os
from lib.track import Track


class DropzoneProgress(progress.ProgressBar):
    def update(self, downloaded, size):
        ratio = int(float(downloaded) / size * 100)
        dz.percent(ratio)

def dragged():
    url = items[0]
    destination = os.environ['path']
    print "Dragged:", url
    print "Destination:", destination

    tempdir = tempfile.gettempdir()

    xml_url = xiami.get_xml_url(*xiami.parse_url(url))
    tracks = xiami.get_tracks(xml_url)

    for i, x in enumerate(tracks):
        dz.begin("Downloading {} of {} track(s)...".format(i, len(tracks)))
        dz.determinate(True)
        progress = DropzoneProgress()
        track = Track(x)
        filename = track.download(tempdir, progress)
        dz.determinate(False)
        track.patch_id3(tempdir, progress)
        shutil.move(os.path.join(tempdir, filename),
                    os.path.join(destination, filename))

    dz.finish('{} track(s) downloaded.'.format(len(tracks)))
    dz.url(False)
