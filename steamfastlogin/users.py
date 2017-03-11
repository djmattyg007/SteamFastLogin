# SteamFastLogin - Login manager for Steam, allowing fast switching between accounts
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

import json
import keyring
from pathlib import Path


KEYRING_NAMESPACE = "steamfastlogin"


class UserList(object):
    def __init__(self, confFile: Path):
        self._confFile = confFile
        self._loadUsers()

    def _loadUsers(self):
        if self._confFile.exists():
            self._usernames = json.loads(self._confFile.read_text(encoding="utf-8"))
        else:
            self._usernames = []

    def _saveUsers(self):
        self._confFile.write_text(json.dumps(self._usernames), encoding="utf-8")

    @property
    def users(self):
        return self._usernames

    def addUser(self, name: str, password: str):
        if name in self._usernames:
            raise Exception("User {0} has already been added".format(name))
        user = User(name)
        user.setPassword(password)
        self._usernames.append(name)
        self._saveUsers()

    def removeUser(self, name: str) -> bool:
        if name in self._usernames:
            user = User(name)
            user.deletePassword()
            self._usernames.remove(name)
            self._saveUsers()
            return True
        return False

    def getUser(self, name: str):
        return User(name)


class User(object):
    def __init__(self, name: str):
        self.name = name

    def setPassword(self, password: str):
        keyring.set_password(KEYRING_NAMESPACE, self.name, password)

    def getPassword(self) -> str:
        return keyring.get_password(KEYRING_NAMESPACE, self.name)

    def deletePassword(self):
        keyring.delete_password(KEYRING_NAMESPACE, self.name)
