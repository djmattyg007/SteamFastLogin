# SteamFastLogin - fast account switcher for Steam
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

import json
from pathlib import Path


class Settings(object):
    def __init__(self, confFile: Path):
        self._confFile = confFile
        self._loadSettings()

    def _loadSettings(self):
        if self._confFile.exists():
            self._settings = json.loads(self._confFile.read_text(encoding="utf-8"))
        else:
            self._settings = {}

    def _saveSettings(self):
        self._confFile.write_text(json.dumps(self._settings), encoding="utf-8")

    def setRawSettings(self, settings: dict):
        self._settings = settings
        self._saveSettings()

    def getRawSettings(self) -> dict:
        return self._settings.copy()

    def getSteamPath(self) -> str:
        if "steam_path" in self._settings:
            return self._settings["steam_path"]
        else:
            return ""
