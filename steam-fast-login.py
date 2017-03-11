#!/usr/bin/python3

# SteamFastLogin - fast account switcher for Steam
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

import sys
from PyQt5.QtWidgets import QApplication
# Importing these DBus classes before instantiating QApplication seems to make
# keyring interactions "Just Work(tm)"
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from steamfastlogin.controller import Controller, AppController
from steamfastlogin.dirs import usersConfFile
from steamfastlogin.gui import MainWindowWidget, UserListWidget, ActionContainerWidget, UserInteraction
from steamfastlogin.users import UserList


def main():
    mainWindow = MainWindowWidget()
    mainWindow.setWindowTitle("Steam Fast Login")

    userList = UserList(usersConfFile())
    ui = UserInteraction(mainWindow)
    controller = Controller(userList, ui)

    userListWidget = UserListWidget()
    # Populate the list with any existing users
    for username in userList.users:
        userListWidget.addItem(username)
    userListWidget.userActivated.connect(controller.loginUser)
    mainWindow.addWidget_(userListWidget)

    actionContainer = ActionContainerWidget()

    appController = AppController(ui, userListWidget, actionContainer, controller)

    mainWindow.addWidget_(actionContainer)

    # Must return the app controller or it gets GC'd
    return appController, mainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Steam Fast Login")
    appController, mainWindow = main()
    mainWindow.show()
    sys.exit(app.exec_())
