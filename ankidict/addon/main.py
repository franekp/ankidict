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

# main window object
from aqt import mw

# with this you can eg. get current module object
from aqt.qt import *
import sys

from libdict import macmillan


def get_plugin():
  return mw.ankidict


class Config(object):
    def __init__(self):
        self.enable_global_shortcut = False
        self.enable_debug_menu = False
        self.deck = 'MillanDict'
        self.model = 'MillanNote'
        self.template = 'MillanTemplate'
        self.shortcut = 'Ctrl+Shift+E'
        # only works at first time!
        # when model is created
        self.note_question = 'Front'
        self.note_answer = 'Back'
        self.note_info = 'Info'
        self.type_answer = True
        self.max_examples_per_sense = 2
        self.examples_hover_area_width = 450
        self.related_defs_panel_width = 250
        self.add_examples_to_list = True
        self.log_wordlist = True
        self.example_style = "text-decoration: none; color: rgb(0, 51, 153);"
        self.enable_old_unused_actions = False


class AnkiDict(object):
    """This should be 'Controller' from the M-V-C pattern."""
    def __init__(self, config):
        mw.ankidict = self
        self.config = config
        self.initialized = False

        # place where we want to place our menu action
        basep = mw.form.menuTools.actions()[6]

        mw.form.menuTools.insertSeparator(basep)

        self.dictact = QAction("Macmillan dictionary", mw)
        self.dictact.setShortcut("Ctrl+D")
        mw.connect(self.dictact, SIGNAL("triggered()"), self.show_dictionary)
        mw.form.menuTools.insertAction(basep, self.dictact)

    def init(self):
        """
        Initializes the dictionary engine if needed.
        Loads some files, etc.
        If called before, does nothing.
        """
        if self.initialized:
            return
        # here can be some initialization
        # return False to say: "Initialization failed"
        from addon.gui import DictWindow
        from addon.collection import Collection
        self.dwnd = DictWindow()
        self.col = Collection()
        self.open_destination("make")
        #MORE
        self.initialized = True
        return True

    def show_dictionary(self):
        """
        Opens dictionary main window.
        """
        self.init()
        self.dwnd.show()

    def add_note_example(self, ex):
        self.col.add_note(*ex.create_anki_note())
        self.dwnd.wordlist_view.add_example(ex)

    def add_note_sense(self, sense):
        """Take a sense or a subsense and add its note to the dict."""
        self.col.add_note(*sense.create_anki_note())
        self.dwnd.wordlist_view.add_sense(sense)

    def open_destination(self, dest):
        """If dest is a string, open a search for it in a dictionary,
        else if it is a Link model instance, open its destination.
        """
        if isinstance(dest, basestring):
            self.dwnd.load_entry(macmillan.query_site(dest))
        else:
            self.dwnd.load_entry(macmillan.query_site(dest.url))
