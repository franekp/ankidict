# -*- coding: utf-8 -*-

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
import macm_parser_css

# windows utilities...

# main dictionary window
class DictWindow(QtGui.QWidget):

	def __init__(self):
		super(DictWindow, self).__init__()
		self.initUI()
		#self.hide()

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
		
		vbox_senses = QtGui.QVBoxLayout()
		vbox_senses.addWidget(QtGui.QLabel("Welcome to our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("Try to use it :p"))
		vbox_senses_widget = QWidget()
		vbox_senses_widget.setLayout(vbox_senses)
		
		scroll_area = QtGui.QScrollArea()
		scroll_area.setWidget(vbox_senses_widget)
		scroll_area.setWidgetResizable(True)
		self.scroll_area = scroll_area
		scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox_head)
		vbox.addWidget(scroll_area)
		# vbox.addStretch(1)
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
		# self.addSomeTestContent()
		dict_entry = macm_parser_css.dict_query(self.search_input.text())
		if isinstance(dict_entry,macm_parser_css.SearchResults):
			# FIXME FIXME FIXME
			self.addSomeTestContent()
			return
		flayout_senses = QtGui.QVBoxLayout()
		for i in dict_entry.senses:
			wk = QtWebKit.QWebView()
			wk.setHtml(i.get_html())
			flayout_senses.addWidget(wk) #, QtGui.QPushButton("ADD"))
			wk.show()
		senses_widget = QWidget()
		senses_widget.setLayout(flayout_senses)
		self.scroll_area.setWidget(senses_widget)
	
	def addSomeTestContent(self):
		vbox_senses = QtGui.QVBoxLayout()
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		vbox_senses.addWidget(QtGui.QLabel("Oh, you pressed return key or the button!"))
		vbox_senses.addWidget(QtGui.QLabel("very good!"))
		vbox_senses.addWidget(QtGui.QLabel("than you for using our addon!"))
		vbox_senses.addWidget(QtGui.QLabel("________________________"))
		
		vbox_senses_widget = QWidget()
		vbox_senses_widget.setLayout(vbox_senses)
		self.scroll_area.setWidget(vbox_senses_widget)

class SenseWidget(QtGui.QWidget):
    # [TODO] stworzyć widget, który będzie wyświetlany w VBoxLayout pokazujący znaczenie
    pass
