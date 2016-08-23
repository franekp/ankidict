import sys

if sys.platform.startswith('win'):
    from PyQt4.QtCore import QSettings
    RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    settings = QSettings(RUN_PATH, QSettings.NativeFormat)
    settings.setValue("Anki", sys.argv[0])

    # to remove that:
    # self.settings.remove("Anki")
