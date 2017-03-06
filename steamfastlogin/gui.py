# SteamFastLogin - fast account switcher for Steam
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from typing import Callable
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QWidget, QLayout, QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtWidgets import QLabel, QLineEdit


_font = QFont()
_font.setPointSize(14)


class MainWindowWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self._layoutContainer = QHBoxLayout(centralWidget)

        self._resetGeometry()

    def _resetGeometry(self):
        self.resize(400, 200)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def addWidget_(self, widget: QWidget):
        if isinstance(widget, QLayout):
            self._layoutContainer.addLayout(widget)
        else:
            self._layoutContainer.addWidget(widget)


class UserListWidget(QListWidget):
    userActivated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._initUI()
        self.itemDoubleClicked.connect(lambda item: self.userActivated.emit(item.text()))

    def _initUI(self):
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setFont(_font)

    def getSelectedUser(self):
        currentItem = self.currentItem()
        if currentItem:
            return currentItem.text()
        else:
            return None

    def removeUserByItem(self, item: QListWidgetItem):
        self.takeItem(self.row(item))

    def enableList(self):
        self.setEnabled(True)

    def disableList(self):
        self.setEnabled(False)


class NewUserForm(QWidget):
    formSubmitted = pyqtSignal(str, str)
    formCancelled = pyqtSignal()
    formClosed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._initUI()
        self._submitted = False

    def _initUI(self):
        grid = QFormLayout()
        grid.setSpacing(10)

        usernameLabel = QLabel("Username")
        usernameLabel.setFont(_font)
        self._usernameField = QLineEdit()
        self._usernameField.setFont(_font)
        grid.addRow(usernameLabel, self._usernameField)

        passwordLabel = QLabel("Password")
        passwordLabel.setFont(_font)
        self._passwordField = QLineEdit()
        self._passwordField.setFont(_font)
        self._passwordField.setEchoMode(QLineEdit.Password)
        grid.addRow(passwordLabel, self._passwordField)

        self._submitButton = QPushButton("Submit")
        self._submitButton.setFont(_font)
        self._submitButton.clicked.connect(lambda e: self.submitForm())
        self._submitButton.setAutoDefault(True)
        grid.addRow(self._submitButton)

        self._usernameField.returnPressed.connect(self._submitButton.click)
        self._passwordField.returnPressed.connect(self._submitButton.click)

        self.setLayout(grid)
        self.setWindowTitle("New User")
        self._resetGeometry()

    def _resetGeometry(self):
        self.resize(350, 150)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        if self._submitted == False:
            self.formCancelled.emit()
        event.accept()
        self.formClosed.emit()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Enter:
            self.submitForm()

    def submitForm(self):
        self._submitted = True
        username = self._usernameField.text()
        password = self._passwordField.text()
        self.close()
        self.formSubmitted.emit(username, password)


class ActionContainerWidget(QVBoxLayout):
    def addButton(self, label: str, callback: Callable):
        button = QPushButton(label)
        button.clicked.connect(callback)
        button.setFont(_font)
        self.addWidget_(button)

    @property
    def buttons(self):
        x = 0
        count = self.count()
        while x < count:
            widget = self.itemAt(x).widget()
            if isinstance(widget, QPushButton):
                yield widget
            x += 1

    def addWidget_(self, widget: QWidget):
        if isinstance(widget, QLayout):
            self.addLayout(widget)
        else:
            self.addWidget(widget, 0, Qt.AlignTop)

    def enableActions(self):
        for button in self.buttons:
            button.setEnabled(True)

    def disableActions(self):
        for button in self.buttons:
            button.setEnabled(False)


class UserInteraction(object):
    def __init__(self, containerWidget: QWidget):
        self._container = containerWidget

    def showInformation(self, title: str, message: str):
        QMessageBox.information(self._container, title, message, QMessageBox.Ok, QMessageBox.Ok)

    def showWarning(self, title: str, message: str):
        QMessageBox.warning(self._container, title, message, QMessageBox.Ok, QMessageBox.Ok)

    def showError(self, title: str, message: str):
        QMessageBox.critical(self._container, title, message, QMessageBox.Ok, QMessageBox.Ok)

    def askQuestion(self, title: str, message: str) -> bool:
        reply = QMessageBox.question(self._container, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        return reply == QMessageBox.Yes
