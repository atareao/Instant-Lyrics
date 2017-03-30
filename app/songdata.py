from bs4 import BeautifulSoup

import requests
from gi.repository import GdkPixbuf

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

GENIUS_TOKEN = 'M36xh_HEiv83IjGTvJmZPy6I2hLhW1TBEdDzpgC1UlB-C9r9jK5juvFzMdo4cRc3'


def get_song_data(song_name, artist_name=''):
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    params = {'q': song_name.strip()}
    json = requests.get('http://api.genius.com/search', params=params, headers=headers).json()

    for hit in json["response"]["hits"]:
        if artist_name == '' or hit["result"]["primary_artist"]["name"].strip().lower() == artist_name.strip().lower():
            song_info = hit['result']
            break

    song = unicode(song_info['title'])
    artist = unicode(song_info['primary_artist']['name'])
    cover_url = unicode(song_info['song_art_image_thumbnail_url'])
    lyrics_url = unicode(song_info['url'])

    return song, artist, cover_url, lyrics_url
    #
    # print query
    # response = requests.get('https://www.googleapis.com/customsearch/v1', params=params).json()
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
    # artist = html.find('a', class_='song_header-primary_info-primary_artist').text
    #
    # return song, artist, cover_url, lyrics


def get_lyrics(url):
    page = requests.get(url)

    html = BeautifulSoup(page.text, "html.parser")

    # remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]

    return unicode(html.select("lyrics p")[0].text)


def get_pixbuf(cover_url, cover_image_size=30):
    loader = GdkPixbuf.PixbufLoader()
    loader.set_size(cover_image_size, cover_image_size)
    loader.write(requests.get(cover_url).content)
    loader.close()

    return loader.get_pixbuf()


def get_lyrics2(song_name):
    song_name += ' metrolyrics'
    name = quote_plus(song_name)
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11'
                         '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    url = 'http://www.google.com/search?q=' + name

    result = requests.get(url, headers=hdr).text
    link_start = result.find('http://www.metrolyrics.com')

    if (link_start == -1):
        return ("Lyrics not found on Metrolyrics")

    link_end = result.find('html', link_start + 1)
    link = result[link_start:link_end + 4]

    lyrics_html = requests.get(link, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel'
                      'Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
                               ).text

    soup = BeautifulSoup(lyrics_html, "lxml")
    raw_lyrics = (soup.findAll('p', attrs={'class': 'verse'}))
    paras = []
    try:
        final_lyrics = unicode.join(u'\n', map(unicode, raw_lyrics))
    except NameError:
        final_lyrics = str.join(u'\n', map(str, raw_lyrics))

    final_lyrics = (final_lyrics.replace('<p class="verse">', '\n'))
    final_lyrics = (final_lyrics.replace('<br/>', ' '))
    final_lyrics = final_lyrics.replace('</p>', ' ')
    return (final_lyrics)


if __name__ == '__main__':
    get_song_data('shape of you ed sheeran')
