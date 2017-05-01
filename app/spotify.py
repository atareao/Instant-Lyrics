import dbus


def get_current_playing_song():
    session_bus = dbus.SessionBus()

    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    song = metadata['xesam:title'].encode('utf-8').decode('utf-8').replace("&", "&amp;")
    artist = metadata['xesam:artist'][0].encode('utf-8').decode('utf-8').replace("&", "&amp;")

    return song, artist
