# -*- coding: utf-8 -*- 

# Macmillan dictionary plugin
# Supports [TODO]:
# * querying Macmillan site
# * caching results from Macmillan dictionary
# * history of searches
# * adding definitions to Anki collection
# * minimized version of Anki for dictionary searches

# main window object
from aqt import mw

# message box if you really want to pass some info to user
from aqt.utils import showInfo

# PyQt library
from aqt.qt import *

# with this you can eg. get current module object
import sys

initialized = False

def init():
  """
  Initializes the dictionary engine if needed.
  Loads some files, etc.
  If called before, does nothing.
  """
  if initialized: return True
  # here can be some initialization
  # return False to say: "Initialization failed"
  return True

def dictionary():
  """
  Opens dictionary main window.
  """
  if not init(): return
  pass

def snippet():
  """
  Shows in right bottom corner of screen window to type queries.
  """
  if not init(): return
  pass

def minimize():
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

def debugger():
  """
  Shows debugging window...
  """
  # You MUST run Anki from terminal to be able to enter debug mode.
  debug()

def global_call():
  """
  Does something on global shortcut...
  """
  # Global shortcuts are NOW WORKING
  showInfo("Global Shortcut call succeeded!")
  pass


# place where we want to place our buttons
basep = mw.form.menuTools.actions()[6]

mw.form.menuTools.insertSeparator(basep)

action = QAction("Macmillan dictionary", mw)
action.setShortcut("Ctrl+D")
mw.connect(action, SIGNAL("triggered()"), dictionary)
mw.form.menuTools.insertAction(basep, action)

acminim = QAction("Hide window", mw)
acminim.setShortcut("Ctrl+M")
mw.connect(acminim, SIGNAL("triggered()"), minimize)
mw.form.menuTools.insertAction(basep, acminim)
 

action2 = QAction("Debug", mw)
mw.connect(action2, SIGNAL("triggered()"), debugger)
mw.form.menuTools.insertAction(basep, action2)

turn_on_global_shortcut_routine = True
if turn_on_global_shortcut_routine:
  import pyqxtgs as gs
  mw.anki_global = gs.PyGlobalShortcutHandler()
  mw.connect(mw.anki_global, SIGNAL('onGlobalShortcut()'), global_call)
  mw.anki_global.setShortcut("Ctrl+Shift+E")
  mw.anki_global.enable()

