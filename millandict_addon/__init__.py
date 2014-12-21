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

# Macmillan dictionary plugin
# Supports [TODO]:
# * querying Macmillan site
# * caching results from Macmillan dictionary
# * history of searches
# * adding definitions to Anki collection
# * minimized version of Anki for dictionary searches

# main window object
from aqt import mw

# with this you can eg. get current module object
from aqt.qt import *
import sys

# window and gui of our addon
import dict_window

def get_plugin():
  return mw.millan

class Config:
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

class MillanDict:
  def __init__(self, config):
    mw.millan = self
    self.config = config
    self.initialized = False

    # place where we want to place our buttons
    basep = mw.form.menuTools.actions()[6]

    mw.form.menuTools.insertSeparator(basep)

    self.dictact = QAction("Macmillan dictionary", mw)
    self.dictact.setShortcut("Ctrl+D")
    mw.connect(self.dictact, SIGNAL("triggered()"), self.dictionary)
    mw.form.menuTools.insertAction(basep, self.dictact)

    self.hideact = QAction("Hide window", mw)
    self.hideact.setShortcut("Ctrl+M")
    mw.connect(self.hideact, SIGNAL("triggered()"), self.minimize)
    mw.form.menuTools.insertAction(basep, self.hideact)

    if config.enable_debug_menu:
      self.dbgact = QAction("Debug", mw)
      mw.connect(self.dbgact, SIGNAL("triggered()"), self.debugger)
      mw.form.menuTools.insertAction(basep, self.dbgact)

    if config.enable_global_shortcut:
      import pyqxtgs as gs
      self.globact = gs.PyGlobalShortcutHandler()
      mw.connect(self.globact, SIGNAL('onGlobalShortcut()'), self.global_call)
      self.globact.setShortcut(self.config.shortcut)
      self.globact.enable()

  def init(self):
    """
    Initializes the dictionary engine if needed.
    Loads some files, etc.
    If called before, does nothing.
    """
    if self.initialized: return True
    # here can be some initialization
    # return False to say: "Initialization failed"
    self.dwnd = dict_window.DictWindow()
    # MORE
    self.initialized = True
    return True

  def dictionary(self):
    """
    Opens dictionary main window.
    """
    if not self.init(): return
    self.dwnd.show()
    pass

  def snippet(self):
    """
    Shows in right bottom corner of screen window to type queries.
    """
    if not self.init(): return
    pass

  def minimize(self):
    """
    Should minimize (hide) the window.
    """
    mw.hide()
    # example usage of showInfo utility
    # uncomment to see, the window is really hidden
    #showInfo("Hidden window!")
    # we should add an icon in notification area to allow unhiding windows
    # then we will be able to remove show call
    mw.show()
    return 0

  def debugger(self):
    """
    Shows debugging window...
    """
    # You MUST run Anki from terminal to be able to enter debug mode.
    debug()

  def global_call(self):
    """
    Does something on global shortcut...
    """
    # Global shortcuts are NOW WORKING
    #showInfo("Global Shortcut call succeeded!")
    print "[ global shortcut handled ]"
    pass
