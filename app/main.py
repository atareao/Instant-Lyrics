import gi
import os
import signal

from lyricwindow import LyricsWindow, get_icon_path

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'lyricsappindicator'


class AppIndicator:
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.main_window = None

        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, get_icon_path('resources/icon.svg'),
                                                    appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

    def build_menu(self):
        menu = Gtk.Menu()

        item_open = Gtk.MenuItem('Open')
        item_open.connect('activate', self.open)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)

        menu.append(item_open)
        menu.append(item_quit)
        menu.show_all()

        return menu

    def open(self, source):
        self.main_window = LyricsWindow()
        self.main_window.show_all()

    def quit(self, source):
        if self.main_window:
            self.main_window.destroy()

        Gtk.main_quit()
        os.kill(os.getpid(), signal.SIGUSR1)


def main():
    app = AppIndicator()
    Gtk.main()

if __name__ == '__main__':
    main()
