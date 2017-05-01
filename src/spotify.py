#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dbus


def get_current_playing_song():
    session_bus = dbus.SessionBus()
    ans = get_current_playing_song_spotify(session_bus)
    if ans is None:
        ans = get_current_playing_song_rhythmbox(session_bus)
    if ans is None:
        raise(Exception)
    return ans


def get_current_playing_song_spotify(session_bus):
    session_bus = dbus.SessionBus()
    try:
        spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                             "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(
            spotify_bus, "org.freedesktop.DBus.Properties")
        metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player",
                                          "Metadata")
        song = str(metadata['xesam:title'])
        artist = str(metadata['xesam:artist'][0])
        return song, artist
    except Exception as e:
        print(e)
    return None


def get_current_playing_song_rhythmbox(session_bus):
    session_bus = dbus.SessionBus()
    try:
        rhythmbox_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.rhythmbox",
            "/org/mpris/MediaPlayer2")
        rhythmbox_properties = dbus.Interface(
            rhythmbox_bus, "org.freedesktop.DBus.Properties")
        metadata = rhythmbox_properties.Get("org.mpris.MediaPlayer2.Player",
                                            "Metadata")
        song = str(metadata['xesam:title'])
        artist = str(metadata['xesam:artist'][0])
        return song, artist
    except Exception as e:
        print(e)
    return None


if __name__ == '__main__':
    print(get_current_playing_song())