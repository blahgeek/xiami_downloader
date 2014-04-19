Xiami.com Downloader
================

Download a single track, collection, album or artist from xiami.com __with lyric__ and __ID3 infomation__ filled.

- Goto [xiami.com](www.xiami.com)
- Find your favorite song, collection etc, copy the url
- Download it!

```
> python xiami.py 'http://www.xiami.com/song/377800?spm=a1z1s.6626001.229054121.10.rZh5X3'
```

```
> python xiami.py -h
usage: xiami.py [-h] [-n] [-d DESTINATION] [-l LYRIC_DESTINATION] URL

Download a single track, collection, album, artist from xiami.com with lyric
and ID3 infomation filled

positional arguments:
  URL                   Xiami url to download, can be
                        song/artist/album/collect

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-lyric        Do not download lyric
  -d DESTINATION, --destination DESTINATION
                        Save path, default to current directory
  -l LYRIC_DESTINATION, --lyric-destination LYRIC_DESTINATION
                        Lyric save path
```
