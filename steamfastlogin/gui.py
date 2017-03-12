# SteamFastLogin - Login manager for Steam, allowing fast switching between accounts
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

import os.path
from typing import Callable
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QWidget
from PyQt5.QtWidgets import QLayout, QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from steamfastlogin.util import tr


_font = QFont()
_font.setPointSize(14)


class IconHolder(object):
    _icon = None
    _sizes = (16, 32, 48, 64, 128, 256)

    @staticmethod
    def getIcon():
        if IconHolder._icon is None:
            IconHolder._icon = QIcon()
            for size in IconHolder._sizes:
                IconHolder._icon.addFile("icons/logo{0}.png".format(size), QSize(size, size))
        return IconHolder._icon


class MainWindowWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.setWindowIcon(IconHolder.getIcon())
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self._layoutContainer = QHBoxLayout(centralWidget)

        self._resetGeometry()

    def _resetGeometry(self):
        self.resize(420, 240)
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
        if currentItem.isSelected():
            return currentItem.text()
        else:
            return None

    def removeUserByItem(self, item: QListWidgetItem):
        self.takeItem(self.row(item))

    def enableList(self):
        self.setEnabled(True)

    def disableList(self):
        self.setEnabled(False)


class AbstractForm(QWidget):
    formCancelled = pyqtSignal()
    formClosed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._initUI()
        self.setWindowIcon(IconHolder.getIcon())
        self._submitted = False

    def _initUI(self):
        raise NotImplementedError("Must implement _initUI()")

    def _resetGeometry(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        if self._submitted == False:
            self.formCancelled.emit()
        event.accept()
        self.formClosed.emit()


class NewUserForm(AbstractForm):
    formSubmitted = pyqtSignal(str, str)

    def _initUI(self):
        grid = QFormLayout()
        grid.setSpacing(10)

        usernameLabel = QLabel(tr("NewUserForm", "Username"))
        usernameLabel.setFont(_font)
        self._usernameField = QLineEdit()
        self._usernameField.setFont(_font)
        grid.addRow(usernameLabel, self._usernameField)

        passwordLabel = QLabel(tr("NewUserForm", "Password"))
        passwordLabel.setFont(_font)
        self._passwordField = QLineEdit()
        self._passwordField.setFont(_font)
        self._passwordField.setEchoMode(QLineEdit.Password)
        grid.addRow(passwordLabel, self._passwordField)

        self._submitButton = QPushButton(tr("NewUserForm", "Submit"))
        self._submitButton.setFont(_font)
        self._submitButton.clicked.connect(lambda e: self.submitForm())
        self._submitButton.setAutoDefault(True)
        grid.addRow(self._submitButton)

        self._usernameField.returnPressed.connect(self._submitButton.click)
        self._passwordField.returnPressed.connect(self._submitButton.click)

        self.setLayout(grid)
        self.setWindowTitle(tr("NewUserForm", "New User"))
        self._resetGeometry()

    def _resetGeometry(self):
        self.resize(350, 150)
        super()._resetGeometry()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Enter:
            self.submitForm()

    def submitForm(self):
        username = self._usernameField.text()
        password = self._passwordField.text()
        if not username or not password:
            QMessageBox.critical(self, tr("NewUserForm", "New User"), tr("NewUserForm", "Must enter username and password"), QMessageBox.Ok, QMessageBox.Ok)
            return
        self._submitted = True
        self.close()
        self.formSubmitted.emit(username, password)


class SettingsForm(AbstractForm):
    formSubmitted = pyqtSignal(dict)

    def _initUI(self):
        self._font = QFont()
        self._font.setPointSize(12)
        self._grid = QVBoxLayout()

        self._form = QFormLayout()
        self._form.setSpacing(8)
        self._fields = {}

        self._addFilePickerField("steam_path", tr("SettingsForm", "Path to Steam"), "Steam (*steam*);;All Files(*)")

        self._grid.addLayout(self._form)

        buttonsContainer = QHBoxLayout()
        buttonsContainer.addStretch(1)
        self._saveButton = QPushButton(tr("SettingsForm", "Save"))
        self._saveButton.setFont(self._font)
        self._saveButton.clicked.connect(lambda e: self.submitForm())
        buttonsContainer.addWidget(self._saveButton)
        self._cancelButton = QPushButton(tr("SettingsForm", "Cancel"))
        self._cancelButton.setFont(self._font)
        self._cancelButton.clicked.connect(self.close)
        buttonsContainer.addWidget(self._cancelButton)
        self._grid.addLayout(buttonsContainer)

        self.setLayout(self._grid)
        self.setWindowTitle(tr("SettingsForm", "Settings"))
        self._resetGeometry()

    def _addFilePickerField(self, code: str, label: str, fileFilter: str):
        labelWidget = QLabel(label)
        labelWidget.setFont(self._font)
        filePicker = QHBoxLayout()
        fieldWidget = QLineEdit()
        fieldWidget.setFont(self._font)
        filePicker.addWidget(fieldWidget)
        fileDialogOpener = QPushButton(QIcon.fromTheme("document-open"), "")
        fileDialogOpener.setFont(self._font)
        fileDialogOpener.setToolTip(tr("SettingsForm", "Pick"))
        filePicker.addWidget(fileDialogOpener)
        def chooseFile(event):
            filename, _ = QFileDialog.getOpenFileName(self, label, os.path.expanduser("~"), fileFilter)
            if filename:
                fieldWidget.setText(filename)
        fileDialogOpener.clicked.connect(chooseFile)
        self._form.addRow(labelWidget, filePicker)
        self._fields[code] = fieldWidget

    def _resetGeometry(self):
        self.resize(450, 150)
        super()._resetGeometry()

    def gatherFormData(self) -> dict:
        data = {}
        for code, field in self._fields.items():
            data[code] = field.text()
        return data

    def setFormData(self, formData: dict):
        for code, field in self._fields.items():
            if code in formData:
                field.setText(formData[code])

    def submitForm(self):
        formData = self.gatherFormData()
        self._submitted = True
        self.close()
        self.formSubmitted.emit(formData)


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
