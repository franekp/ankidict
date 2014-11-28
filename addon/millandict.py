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

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore

# with this you can eg. get current module object
import sys

turn_on_global_shortcut_routine = True

deck = 'MillanDict'

initialized = False

def init():
  """
  Initializes the dictionary engine if needed.
  Loads some files, etc.
  If called before, does nothing.
  """
  global initialized
  if initialized: return True
  # here can be some initialization
  # return False to say: "Initialization failed"
  mw.dwnd = DictWindow()
  # MORE
  initialized = True
  return True

def dictionary():
  """
  Opens dictionary main window.
  """
  if not init(): return
  mw.dwnd.show()
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
  #showInfo("Global Shortcut call succeeded!")
  pass

def add_card(q, a):
  # adds card to collection
  # creates deck if not existing and return id
  global deck
  did = mw.col.decks.id(deck)
  # selects deck - why? [TODO]
  mw.col.decks.select(did)
  # gets deck object
  dck = mw.col.decks.get(did)

  card = get_card(q)
  if card != None:
    # [TODO] modify answer
    pass
  else:
    # [TODO] add card
    pass

def get_card(q):
  # returns card with selected question
  # [TODO] all
  return None

def is_card(q, a):
  # checks if the question is in collection
  # [TODO] check if q is in collection and a in it's answers
  return False

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

if turn_on_global_shortcut_routine:
  import pyqxtgs as gs
  mw.anki_global = gs.PyGlobalShortcutHandler()
  mw.connect(mw.anki_global, SIGNAL('onGlobalShortcut()'), global_call)
  mw.anki_global.setShortcut("Ctrl+Shift+E")
  mw.anki_global.enable()


# windows utilities...

# main dictionary window
class DictWindow(QtGui.QWidget):

	def __init__(self):
		super(DictWindow, self).__init__()
		self.initUI()

	def initUI(self):
		# QLineEdit
		# QWebView
		search_input = QLineEdit()
		search_button = QtGui.QPushButton("SEARCH")
		search_input.returnPressed.connect(self.dictSearchEvent)
		search_button.clicked.connect(self.dictSearchEvent)

		self.search_input = search_input

		hbox_head = QtGui.QHBoxLayout()
		#hbox.addStretch(1)
		hbox_head.addWidget(search_input)
		hbox_head.addWidget(search_button)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox_head)
		vbox.addStretch(1)
		self.setLayout(vbox)
		#self.setGeometry(300, 300, 300, 150)
		self.resize(800,600)
		self.setWindowTitle('Macmillan Dictionary')
		self.show()

	def closeEvent(self, event):
		event.ignore()
		self.hide()

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			# Selecting the search input field
			print "ESC key pressed!"
			self.search_input.setFocus()
			pass

	def dictSearchEvent(self):
		# TODO - working with MacMillan wrapper
		print "dictSearchEvent() called!"
		pass

class SenseWidget(QtGui.QWidget):
    # [TODO] stworzyć widget, który będzie wyświetlany w VBoxLayout pokazujący znaczenie
    pass
