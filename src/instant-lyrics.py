#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk

import signal
import threading

from windows import LyricsWindow, PreferenceWindow
import utils
import comun


class AppIndicator():

    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        indicator = appindicator.Indicator.new(
            comun.APPINDICATOR_ID,
            comun.ICON,
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())

        self.Config = utils.get_config()
        Gtk.main()

    def build_menu(self):
        menu = Gtk.Menu()

        get_lyrics = Gtk.MenuItem('Get Lyrics')
        get_lyrics.connect('activate', self.fetch_lyrics)

        spotify_lyrics = Gtk.MenuItem('Spotify Lyrics')
        spotify_lyrics.connect('activate', self.spotify_lyrics)

        preferences = Gtk.MenuItem('Preferences')
        preferences.connect('activate', self.preferences)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)

        menu.append(get_lyrics)
        menu.append(spotify_lyrics)
        menu.append(preferences)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def fetch_lyrics(self, source):
        LyricsWindow("get", self)

    def spotify_lyrics(self, source):
        win = LyricsWindow("spotify", self)
        thread = threading.Thread(target=win.get_spotify)
        thread.daemon = True
        thread.start()

    def preferences(self, source):
        PreferenceWindow(self)

    def quit(self, source):
        Gtk.main_quit()


if __name__ == '__main__':
    app = AppIndicator()
