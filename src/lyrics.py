#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from lxml.html import fromstring
from urllib.parse import quote_plus


def get_lyrics(song_name):

    song_name += ' metrolyrics'
    name = quote_plus(song_name)
    url = 'http://www.google.com/search?q=' + name
    result = requests.get(url).text
    link_start = result.find('http://www.metrolyrics.com')
    if(link_start == -1):
        return('Lyrics not found on Metrolyrics')
    link_end = result.find('html', link_start + 1)
    link = result[link_start:link_end + 4]

    r = requests.get(link)
    lyrics_html = r.content.decode('UTF-8')

    doc = fromstring(lyrics_html)
    ly = '\n'.join(verso.text_content() for verso in doc.cssselect('p.verse'))
    return (ly)


if __name__ == '__main__':
    print(get_lyrics('Despacito'))
