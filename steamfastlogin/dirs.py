# SteamFastLogin - fast account switcher for Steam
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from appdirs import AppDirs
from pathlib import Path


dirs = AppDirs("steam-fast-login")


def confDir() -> Path:
    cdir = Path(dirs.user_config_dir)
    cdir.mkdir(mode=0o750, parents=True, exist_ok=True)
    return cdir


def usersConfFile() -> Path:
    cdir = confDir()
    return cdir / "users.json"


def settingsConfFile() -> Path:
    cdir = confDir()
    return cdir / "settings.json"
