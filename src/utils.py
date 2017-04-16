#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configparser
from comun import CONFIG_PATH


def create_default_config():
    if not os.path.isdir(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH))

    Config = configparser.ConfigParser()
    Config.add_section('Main')
    Config.set('Main', "window width", "350")
    Config.set('Main', "window height", "650")

    with open(CONFIG_PATH, 'w') as config_file:
        Config.write(config_file)


def get_config():
    if not os.path.isfile(CONFIG_PATH):
        create_default_config()
    Config = configparser.ConfigParser()
    Config.read(CONFIG_PATH)
    return Config


if __name__ == '__main__':
    print(CONFIG_PATH)
    if not os.path.isdir(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH))
    config = get_config()
    print(config)
