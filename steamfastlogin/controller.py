# SteamFastLogin - fast account switcher for Steam
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from steamfastlogin.gui import MainWindowWidget, UserListWidget, NewUserForm, ActionContainerWidget, UserInteraction
from steamfastlogin.users import UserList


class Controller(object):
    def __init__(self, userList: UserList, ui: UserInteraction):
        self._userList = userList
        self._ui = ui

    def addUser(self, name: str, password: str):
        try:
            self._userList.addUser(name, password)
        except Exception as e:
            self._ui.showError("Error", str(e))
            return False
        return True

    def removeUser(self, name: str):
        reply = self._ui.askQuestion("Remove User", "Are you sure you want to remove user '{0}'?".format(name))
        if reply:
            try:
                self._userList.removeUser(name)
            except Exception as e:
                self._ui.showError("Error", str(e))
                return False
            return True
        else:
            return False

    def loginUser(self, name: str):
        user = self._userList.getUser(name)
        print("log in", user.name, user.getPassword())


class AppController(object):
    def __init__(self, ui: UserInteraction, userList: UserListWidget, actions: ActionContainerWidget, controller: Controller):
        self._ui = ui
        self._userList = userList
        self._actions = actions
        self._controller = controller

        self._initAppActions()

    def _initAppActions(self):
        self._actions.addButton("&Login", self.login)
        self._actions.addButton("&Add", self.add)
        self._actions.addButton("&Remove", self.remove)

    def login(self, event):
        selectedUser = self._userList.getSelectedUser()
        if selectedUser:
            self._controller.loginUser(selectedUser)
        else:
            self._ui.showWarning("Login", "No user selected")

    def _addSubmitCallback(self, username: str, password: str):
        result = self._controller.addUser(username, password)
        if result:
            self._userList.addItem(username)

    def add(self, event):
        self._actions.disableActions()
        self._userList.disableList()

        addUserForm = NewUserForm()
        addUserForm.formSubmitted.connect(self._addSubmitCallback)
        addUserForm.formClosed.connect(lambda: self._actions.enableActions())
        addUserForm.formClosed.connect(lambda: self._userList.enableList())

        addUserForm.show()

    def remove(self, event):
        selectedUser = self._userList.getSelectedUser()
        if selectedUser:
            result = self._controller.removeUser(selectedUser)
            if result:
                self._userList.removeUserByItem(self._userList.currentItem())
        else:
            self._ui.showWarning("Remove User", "No user selected")
