# SteamFastLogin - fast account switcher for Steam
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from steamfastlogin.gui import UserListWidget, NewUserForm, SettingsForm, ActionContainerWidget, UserInteraction
from steamfastlogin.settings import Settings
from steamfastlogin.users import UserList
from steamfastlogin.util import tr, ProcessRunner


class Controller(object):
    def __init__(self, settings: Settings, userList: UserList, ui: UserInteraction, processRunner: ProcessRunner):
        self._settings = settings
        self._userList = userList
        self._ui = ui
        self._processRunner = processRunner

    def addUser(self, name: str, password: str):
        try:
            self._userList.addUser(name, password)
        except Exception as e:
            self._ui.showError(tr("Controller", "Error"), tr("Controller", str(e)))
            return False
        return True

    def removeUser(self, name: str):
        reply = self._ui.askQuestion(tr("Controller", "Remove User"), tr("Controller", "Are you sure you want to remove user '{0}'?").format(name))
        if reply:
            try:
                self._userList.removeUser(name)
            except Exception as e:
                self._ui.showError(tr("Controller", "Error"), str(e))
                return False
            return True
        else:
            return False

    def loginUser(self, name: str):
        user = self._userList.getUser(name)
        self._processRunner.runAsync(self._getSteamCommand(), ("-login", user.name, user.getPassword()))

    def closeSteam(self):
        reply = self._ui.askQuestion(tr("Controller", "Close Steam"), tr("Controller", "Are you sure?"))
        if reply:
            self._processRunner.runAsync(self._getSteamCommand(), ("-shutdown",))

    def _getSteamCommand(self):
        command = self._settings.getSteamPath()
        if not command:
            command = "steam"
        return command


class AppController(object):
    def __init__(self, settings: Settings, ui: UserInteraction, userList: UserListWidget, actions: ActionContainerWidget, controller: Controller):
        self._settings = settings
        self._ui = ui
        self._userList = userList
        self._actions = actions
        self._controller = controller

        self._initAppActions()

    def _initAppActions(self):
        self._actions.addButton(tr("AppController", "&Login"), self.login)
        self._actions.addButton(tr("AppController", "&Add"), self.add)
        self._actions.addButton(tr("AppController", "&Remove"), self.remove)
        self._actions.addButton(tr("AppController", "&Close Steam"), self.close)
        self._actions.addButton(tr("AppController", "&Settings"), self.settings)

    def login(self, event):
        selectedUser = self._userList.getSelectedUser()
        if selectedUser:
            self._controller.loginUser(selectedUser)
        else:
            self._ui.showWarning(tr("AppController", "Login"), tr("AppController", "No user selected"))

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
            self._ui.showWarning(tr("AppController", "Remove User"), tr("AppController", "No user selected"))

    def close(self, event):
        self._controller.closeSteam()

    def _settingsSaveCallback(self, formData: dict):
        self._settings.setRawSettings(formData)

    def settings(self, event):
        self._actions.disableActions()
        self._userList.disableList()

        settingsForm = SettingsForm()
        settingsForm.setFormData(self._settings.getRawSettings())
        settingsForm.formSubmitted.connect(self._settingsSaveCallback)
        settingsForm.formClosed.connect(lambda: self._actions.enableActions())
        settingsForm.formClosed.connect(lambda: self._userList.enableList())

        settingsForm.show()
