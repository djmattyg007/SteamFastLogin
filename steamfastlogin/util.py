# SteamFastLogin - Login manager for Steam, allowing fast switching between accounts
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from typing import Optional
from PyQt5.QtCore import QCoreApplication, QProcess


def tr(ctx: str, msg: str, disambiguation: Optional[str]=None) -> str:
    return QCoreApplication.translate(ctx, msg, disambiguation)


class ProcessRunner(object):
    def runAsync(self, command: str, args: tuple):
        QProcess.startDetached(command, args)
