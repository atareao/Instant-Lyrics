#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
try:
    gi.require_version('GdkPixbuf', '2.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import GdkPixbuf
import lxml.html as lh
import requests


GENIUS_TOKEN = '\
M36xh_HEiv83IjGTvJmZPy6I2hLhW1TBEdDzpgC1UlB-C9r9jK5juvFzMdo4cRc3'


def get_song_data(song_name, artist_name=''):
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    params = {'q': song_name.strip()}
    json = requests.get('http://api.genius.com/search', params=params,
                        headers=headers).json()
    for hit in json["response"]["hits"]:
        if artist_name == '' or \
                hit["result"]["primary_artist"]["name"].strip().lower() == \
                artist_name.strip().lower():
            song_info = hit['result']
            break
    song = song_info['title']
    artist = song_info['primary_artist']['name']
    cover_url = song_info['song_art_image_thumbnail_url']
    lyrics_url = song_info['url']
    return song, artist, cover_url, lyrics_url
    #
    # print query
    # response = requests.get('https://www.googleapis.com/customsearch/v1',
    #                         params=params).json()
    # print response
    # items = response['items']
    # print items[0]
    # url = items[0]['link']
    # print url
    #
    # page = requests.get(url)
    #
    # html = BeautifulSoup(page.text, "html.parser")
    #
    # # remove script tags that they put in the middle of the lyrics
    # [h.extract() for h in html('script')]
    #
    # # at least Genius is nice and has a tag called 'lyrics'!
    # lyrics = html.select("lyrics p")[0].text
    #
    # cover_url = html.find('img', class_='cover_art-image')['src']
    # song = html.find('h1', class_='song_header-primary_info-title').text
    # artist = html.find(
    #   'a', class_='song_header-primary_info-primary_artist').text
    #
    # return song, artist, cover_url, lyrics


'''
def get_lyrics2(url):
    print('============')
    print(url)
    page = requests.get(url)

    html = BeautifulSoup(page.text, "html.parser")

    # remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]

    return html.select("lyrics p")[0].text
'''


def get_lyrics(url):
    phrases = []
    page = requests.get(url)
    doc = lh.fromstring(page.text)
    for div in doc.cssselect('.lyrics'):
        phrases.append(div.text_content().strip())
    ans = ''.join(phrases)
    return ans


def get_pixbuf(cover_url, cover_image_size=30):
    loader = GdkPixbuf.PixbufLoader()
    loader.set_size(cover_image_size, cover_image_size)
    loader.write(requests.get(cover_url).content)
    loader.close()

    return loader.get_pixbuf()


if __name__ == '__main__':
    # get_song_data('shape of you ed sheeran')
    print(get_lyrics(
        'https://genius.com/Amaia-montero-los-abrazos-rotos-lyrics'))
