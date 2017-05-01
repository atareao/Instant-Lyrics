#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of instant-lyrics
#
# Copyright (C) 2017
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os


def is_package():
    return __file__.find('src') < 0


APP = 'instant-lyrics'
APPNAME = APP
APP_CONF = APP + '.conf'
CONFIG_PATH = os.path.join(os.getenv("HOME"), '.config', APP, 'config')

# check if running from source
if is_package():
    ROOTDIR = os.path.join('/opt/extras.ubuntu.com/', APP)
    APPDIR = os.path.join(ROOTDIR, 'share', APP)
    CHANGELOG = os.path.join(APPDIR, 'changelog')
    ICONDIR = os.path.join(ROOTDIR, 'share/icons')
    AUTOSTART = os.path.join(APPDIR,
                             'instant-lyrics-autostart.desktop')
    UIDIR = os.path.join(APPDIR, 'ui')
else:
    ROOTDIR = os.path.dirname(__file__)
    APPDIR = ROOTDIR
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')
    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
    AUTOSTART = os.path.join(APPDIR,
                             'instant-lyrics-autostart.desktop')
    UIDIR = os.path.join(APPDIR, 'ui')
f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'

ICON = os.path.join(ICONDIR, APP + '.svg')
SPOTIFY_ICON = os.path.join(ICONDIR, 'spotify-logo-symbolic.svg')
UIFILE = os.path.join(UIDIR, 'ToolbarInfo.ui')
APPINDICATOR_ID = 'lyricsappindicator'
