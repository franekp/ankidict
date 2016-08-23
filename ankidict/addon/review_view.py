# -*- coding: utf-8 -*-

####
# Copyright (c) 2014 Wojciech Kordalski
# Copyright (c) 2014 Franciszek Piszcz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####

from datetime import datetime

from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl

from addon.main import get_plugin
from addon.reviewer import Reviewer


class ReviewView(QWidget):
    def __init__(self, daily_review_time, poll_interval_seconds):
        super(ReviewView, self).__init__()
        self.setWindowFlags(
            self.windowFlags()
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Popup
            # | QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
        )
        from aqt import mw
        self.webview = QWebView()
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setMargin(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(self.webview)
        self.reviewer = Reviewer(mw.col, self)
        self.setLayout(self.main_layout)
        self.reload()
        self.is_active = False
        # hour and minute of the day to show reviews
        self.hour = int(daily_review_time.split(":")[0])
        self.minute = int(daily_review_time.split(":")[1])
        self.last_reviewed_date = "<never>"
        self.poll_interval_ms = poll_interval_seconds * 1000
        # start controlling time when show reviews:
        QtCore.QTimer.singleShot(
            self.poll_interval_ms, self.maintain_background
        )

    def maintain_background(self):
        """Background procedure that is called every <some time interval> and
        checks whether there is time to review vocabulary. If it is, then
        activates the review_view window.
        """
        now = datetime.now()
        if now.hour < self.hour:
            QtCore.QTimer.singleShot(
                self.poll_interval_ms, self.maintain_background)
            return
        if now.hour == self.hour and now.minute < self.minute:
            QtCore.QTimer.singleShot(
                self.poll_interval_ms, self.maintain_background)
            return
        # it is after the time of day when reviews should be shown
        # check whether this was already done today:
        today = "%d-%d-%d" % (now.year, now.month, now.day)
        if self.last_reviewed_date == today:
            QtCore.QTimer.singleShot(
                self.poll_interval_ms, self.maintain_background)
            return
        # reviews were not yet done today:
        self.last_reviewed_date = today
        QtCore.QTimer.singleShot(
            self.poll_interval_ms, self.maintain_background)
        self.activate()

    def reload(self):
        self.webview.load(QUrl("http://localhost:9090/"))

    def activate(self):
        self.is_active = True
        desktop_w = QtGui.QApplication.desktop().width()
        desktop_h = QtGui.QApplication.desktop().height()
        my_w = desktop_w * 0.97
        my_h = desktop_h * 0.9
        self.resize(my_w, my_h)
        x = desktop_w/2 - my_w/2
        y = desktop_h/2 - my_h/2
        self.move(x, y)
        self.maintain()
        self.reload()

    def maintain(self):
        self.show()
        self.activateWindow()
        # możliwe, że przydatne do lepszego blokowania:
        # http://doc.qt.io/qt-4.8/qwidget.html#grabKeyboard
        # http://doc.qt.io/qt-4.8/qwidget.html#grabMouse
        self.setFocus()
        self.webview.setFocus()
        self.webview.page().mainFrame().setFocus()
        if self.is_active:
           QtCore.QTimer.singleShot(100, self.maintain)
        else:
           self.hide()

    def deactivate(self):
        self.is_active = False
