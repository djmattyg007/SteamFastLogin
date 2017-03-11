#!/usr/bin/python3

# SteamFastLogin - Login manager for Steam, allowing fast switching between accounts
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

import sys
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication
# Importing these DBus classes before instantiating QApplication seems to make
# keyring interactions "Just Work(tm)"
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from steamfastlogin.controller import Controller, AppController
from steamfastlogin.dirs import usersConfFile, settingsConfFile
from steamfastlogin.gui import MainWindowWidget, UserListWidget, ActionContainerWidget, UserInteraction
from steamfastlogin.settings import Settings
from steamfastlogin.users import UserList
from steamfastlogin.util import tr, ProcessRunner


def guiInit():
    userList = UserList(usersConfFile())
    settings = Settings(settingsConfFile())

    mainWindow = MainWindowWidget()
    mainWindow.setWindowTitle(tr("guiInit", "Steam Fast Login"))

    ui = UserInteraction(mainWindow)
    controller = Controller(settings, userList, ui, ProcessRunner())

    userListWidget = UserListWidget()
    # Populate the list with any existing users
    for username in userList.users:
        userListWidget.addItem(username)
    userListWidget.userActivated.connect(controller.loginUser)
    mainWindow.addWidget_(userListWidget)

    actionContainer = ActionContainerWidget()

    appController = AppController(settings, ui, userListWidget, actionContainer, controller)

    mainWindow.addWidget_(actionContainer)

    # Must return the app controller or it gets GC'd
    return appController, mainWindow


def main(argv=None):
    if argv is None:
        argv = sys.argv

    app = QApplication(argv)
    app.installTranslator(QTranslator())
    app.setApplicationName(tr("main", "Steam Fast Login"))
    appController, mainWindow = guiInit()
    mainWindow.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
