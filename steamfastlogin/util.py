from PyQt5.QtCore import QProcess


class ProcessRunner(object):
    def runAsync(self, command: str, args: tuple):
        QProcess.startDetached(command, args)
