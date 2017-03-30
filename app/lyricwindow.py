import gi
import os
from threading import Thread

from requests import RequestException

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

from periodicthread import PeriodicThread
from songdata import get_song_data, get_pixbuf, get_lyrics
from spotify import get_current_playing_song
from messages import Error


def get_icon_path(rel_path):
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource


def bind_accelerator(accelerators, widget, accelerator, signal='clicked'):
    key, mod = Gtk.accelerator_parse(accelerator)
    widget.add_accelerator(signal, accelerators, key, mod, Gtk.AccelFlags.VISIBLE)


class LyricsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Lyrics")
        self.set_icon_from_file(get_icon_path('resources/icon.svg'))
        # self.set_icon_name('spotify-logo-symbolic')
        self.set_border_width(0)
        self.set_default_size(470, 650)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.init_spotify_checker()

        accelerators = Gtk.AccelGroup()
        self.add_accel_group(accelerators)
        self.connect('key_press_event', self._check_escape)

        self.spinner = Gtk.Spinner()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.main_box.set_size_request(350, 700)

        lyrics_vbox = self._create_lyrics_box()
        self.main_box.pack_start(lyrics_vbox, True, True, 0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.main_box)

        self.toolbar = Toolbar(self.on_lyric_requested, self.on_cancel_spotify, accelerators, scrolled)
        self.set_titlebar(self.toolbar)

        self.add(scrolled)
        self.toolbar.btn_spotify.emit('clicked')

    def init_spotify_checker(self):
        self.spotify_checker = PeriodicThread(self.load_from_spotify, 0.5)
        self._last_song_hash = ''

    def on_lyric_requested(self, is_from_spotify, song, artist_name=''):
        if is_from_spotify:
            if not self.spotify_checker.isAlive():
                self.spotify_checker = PeriodicThread(self.load_from_spotify, 0.5)
                self.spotify_checker.start()
        else:
            self.spotify_checker.cancel()
            self._last_song_hash = ''
            self.toolbar.info.clear()
            self.start_fetching_song_data(song, artist_name)

    def on_cancel_spotify(self):
        self.spotify_checker.cancel()

    def show_error_msg(self, title, message):
        self.status.set_markup('<b>' + title + '</b>')
        self.message.set_text(message)

    def clear_error_msg(self):
        self.show_error_msg('', '')

    def clear_box(self):
        self.lyrics.set_text('')
        self.clear_error_msg()

    def _check_escape(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            result = True
            result &= self.toolbar.do_escape()
            return result

        return False

    def _create_lyrics_box(self):
        lyrics_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.title = Gtk.Label()
        self.title.set_justify(Gtk.Justification.CENTER)

        self.lyrics = Gtk.Label()
        self.lyrics.set_justify(Gtk.Justification.LEFT)
        self.lyrics.set_property("margin_left", 50)
        self.lyrics.set_property("margin_right", 50)
        self.lyrics.set_line_wrap(True)

        self.status = Gtk.Label()
        self.status.set_justify(Gtk.Justification.CENTER)
        self.status.set_property("margin_left", 50)
        self.status.set_property("margin_right", 50)

        self.message = Gtk.Label()
        self.message.set_justify(Gtk.Justification.CENTER)
        self.message.set_property("margin_left", 50)
        self.message.set_property("margin_right", 50)

        lyrics_vbox.pack_start(self.title, False, False, 5)
        lyrics_vbox.pack_start(self.spinner, False, False, 5)
        lyrics_vbox.pack_start(self.lyrics, False, False, 5)
        lyrics_vbox.pack_start(self.status, False, False, 5)
        lyrics_vbox.pack_start(self.message, False, False, 5)
        lyrics_vbox.set_size_request(350, 700)

        return lyrics_vbox

    def load_from_spotify(self):
        try:
            song, artist = get_current_playing_song()

            song_hash = hash((song, artist))
            if self._last_song_hash == song_hash:
                return

            self._last_song_hash = song_hash
            self.toolbar.info.set_song(song, artist)
        except:
            self.clear_box()
            self.show_error_msg(Error.Spotify.title, Error.Spotify.message)
            return

        self.start_fetching_song_data(song, artist)

    def start_fetching_song_data(self, song_name, artist_name=''):
        self.clear_box()

        t = Thread(target=self._load_song_data, args=[song_name, artist_name])
        t.daemon = True
        t.start()

    def _load_song_data(self, song_name, artist_name):
        self.spinner.start()
        try:
            song, artist, cover, lyrics_url = get_song_data(song_name, artist_name)
            self.toolbar.info.set_song(song, artist)
            self.toolbar.btn_search.set_active(False)

            lt = Thread(target=lambda x: self.lyrics.set_text(get_lyrics(lyrics_url)), args=[None])
            lt.start()

            ct = Thread(target=lambda x: self.toolbar.info.set_cover(get_pixbuf(cover)), args=[None])
            ct.start()

            lt.join()
            ct.join()

            self.spinner.stop()
        except RequestException:
            self.show_error_msg(Error.Request.title, Error.Request.message)
            self._last_song_hash = ''
        except:
            self.show_error_msg(Error.NotFound.title, Error.NotFound.message)

        self.spinner.stop()


class Toolbar(Gtk.HeaderBar):
    def __init__(self, lyric_request_callback, cancel_spotify_callback, accelerators, spinner, **properties):
        super(Toolbar, self).__init__(**properties)
        self.set_show_close_button(True)
        self.set_custom_title(None)

        self.request_lyric = lyric_request_callback
        self.cancel_spotify = cancel_spotify_callback
        self.accelerators = accelerators

        self.an = Gtk.Entry()
        self.searchbar = None
        self.spinner = spinner

        self.info = ToolbarInfo()
        self.pack_start(self.info)

        self.btn_search = self._create_search_btn()
        self.pack_end(self.btn_search)

        self.btn_spotify = self._create_spotify_btn()
        self.pack_end(self.btn_spotify)

    def do_escape(self):
        if self.btn_search.get_active():
            self.btn_search.emit('clicked')
            return True

        return False

    def show_search_bar(self):
        self.info.hide()
        if self.searchbar:
            self.searchbar.show()

    def show_info_bar(self):
        if self.searchbar:
            self.searchbar.hide()
        self.info.show()

    def _on_search_btn_clicked(self, widget):
        if not self.searchbar:
            self.searchbar = self._create_search_bar()
            self.pack_start(self.searchbar)

        if self.btn_search.get_active():
            self.show_search_bar()
            self.searchbar.set_property('margin_top', 3)
            self.searchbar.set_property('margin_bottom', 2)
            self.searchbar.grab_focus()
        else:
            self.show_info_bar()

    def _on_spotify_btn_clicked(self, widget):
        if self.btn_spotify.get_active():
            self.info.clear()
            self.show_info_bar()
            self.request_lyric(True, '')
            self.btn_search.set_active(False)
        else:
            self.cancel_spotify()

    def _on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Return:
            if len(self.searchbar.get_text()) > 0:
                lst = self.searchbar.get_text().split('/')
                self.request_lyric(False, unicode(lst[0].strip()), unicode(lst[1].strip()) if len(lst) > 1 else '')
                self.btn_spotify.set_active(False)
                self.spinner.grab_focus()

    def _create_search_btn(self):
        btn_search = Gtk.ToggleButton()
        btn_search.add(Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="edit-find-symbolic"), Gtk.IconSize.BUTTON))
        btn_search.connect('clicked', self._on_search_btn_clicked)
        bind_accelerator(self.accelerators, btn_search, '<Control>f')

        return btn_search

    def _create_spotify_btn(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('resources/spotify-logo-symbolic.svg', 16, 16)
        Gtk.IconTheme.add_builtin_icon("spotify-logo-symbolic", -1, pixbuf)

        btn_spotify = Gtk.ToggleButton()
        btn_spotify.add(Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="spotify-logo-symbolic"), Gtk.IconSize.BUTTON))
        btn_spotify.connect('clicked', self._on_spotify_btn_clicked)
        bind_accelerator(self.accelerators, btn_spotify, '<Control>o')

        return btn_spotify

    def _create_search_bar(self):
        searchbar = Gtk.Entry()
        searchbar.connect('key-release-event', self._on_key_release)
        searchbar.set_property('margin_top', 2)

        return searchbar


class ToolbarInfo(Gtk.Bin):
    def __init__(self, **properties):
        super(ToolbarInfo, self).__init__(**properties)

        builder = Gtk.Builder()
        builder.add_from_file('ui/ToolbarInfo.ui')

        self.infobox = builder.get_object('info')
        self.add(self.infobox)

        self.labels_container = builder.get_object('nowplaying_labels')

        self.cover = builder.get_object('cover')
        self.song = builder.get_object('title')
        self.artist = builder.get_object('artist')

    def set_song(self, song, artist=''):
        self.clear()

        self.song.set_text(song)
        self.artist.set_text(artist)

    def set_cover(self, cover=None):
        self.cover.set_from_pixbuf(cover)

    def clear(self):
        self.song.set_text('')
        self.artist.set_text('')
        self.set_cover(None)
