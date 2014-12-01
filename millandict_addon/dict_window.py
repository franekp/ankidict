# -*- coding: utf-8 -*-

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
import macm_parser_css

# TODO LIST:

# - related definitions:
#		- add it to UI
#		- eat also the href attrs from the html of 'related defs' (change in parser)
# - add SearchResults to UI
# - add intro_paragraph to UI
# - ('remove' button / edit mode) in the word list

# - some word list management (e.g. shuffle or save to file)
# - add better key phrase removal from the definitions (e.g. remove also words with 's' at the end) 

# windows utilities...

# main dictionary window
class DictWindow(QtGui.QWidget):

	def __init__(self):
		super(DictWindow, self).__init__()
		self.initUI()
		#self.hide()
		self.dictSearchEvent()
		self.saved_senses = []

	def initUI(self):
		# QLineEdit
		# QWebView
		search_input = QLineEdit("make")
		search_button = QtGui.QPushButton("SEARCH")
		saved_senses_view_button = QtGui.QPushButton("LIST")
		search_input.returnPressed.connect(self.dictSearchEvent)
		search_button.clicked.connect(self.dictSearchEvent)
		saved_senses_view_button.clicked.connect(self.viewSavedSenses)
		
		self.search_input = search_input
		
		hbox_head = QtGui.QHBoxLayout()
		#hbox.addStretch(1)
		hbox_head.addWidget(search_input)
		hbox_head.addWidget(search_button)
		hbox_head.addWidget(saved_senses_view_button)
		
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
		
		self.related_defs_scroll_area = QScrollArea()
		self.related_defs_scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		
		hbox_tail = QHBoxLayout()
		hbox_tail.addWidget(scroll_area)
		hbox_tail.addWidget(self.related_defs_scroll_area)
		
		vbox.addLayout(hbox_tail)
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
			self.search_input.setText("")
			pass

	def dictSearchEvent(self):
		# TODO - working with MacMillan wrapper
		print "dictSearchEvent() called!"
		# self.addSomeTestContent()
		dict_entry = macm_parser_css.dict_query(self.search_input.text())
		self.dict_entry = dict_entry
		if isinstance(dict_entry,macm_parser_css.SearchResults):
			vbox_results = QVBoxLayout()
			def results_element_clicked(i):
				def func():
					self.search_input.setText(i)
					self.dictSearchEvent()
				return func
			for (title, href) in dict_entry.links:
				btn = QPushButton(title)
				vbox_results.addWidget(btn)
				btn.clicked.connect(results_element_clicked(href))
			widget_results = QWidget()
			widget_results.setLayout(vbox_results)
			self.scroll_area.setWidget(widget_results)
			return
		
		# senses definitions and phrases:
		flayout_senses = QtGui.QVBoxLayout()
		def save_sense(i):
			def tmp():
				self.saved_senses += [i]
			return tmp
		d_entry_all = dict_entry.senses + dict_entry.phrases
		for i in d_entry_all:
			wk = QtWebKit.QWebView()
			wk.setHtml(i.get_html())
			btn = QtGui.QPushButton("ADD")
			
			def save_sense_old():
				self.saved_senses += [i]
			btn.clicked.connect(save_sense(i))
			
			btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
			wk.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
			wk.setMinimumHeight(100)
			
			wp = QWebPage()
			wp.mainFrame().setHtml(i.get_html())
			tmp_size = wp.mainFrame().contentsSize()
			def adjust_height(h):
				if h < 80:
					h = 80
				if h < 120:
					return h/7 + 40
				else:
					return h/11 + 40
			tmp_size.setHeight(adjust_height(tmp_size.height()))
			
			wk.setMinimumSize(tmp_size)
			#print tmp_size
			
			tmp_layout = QHBoxLayout()
			tmp_layout.addWidget(wk)
			tmp_layout.addWidget(btn)
			flayout_senses.addLayout(tmp_layout)
			wk.show()
			
		senses_widget = QWidget()
		senses_widget.setLayout(flayout_senses)
		self.scroll_area.setWidget(senses_widget)
		
		# related defs:
		vbox_related = QVBoxLayout()
		def related_clicked(href):
			def func():
				self.search_input.setText(href)
				self.dictSearchEvent()
			return func
		for (title, href) in dict_entry.related:
			btn = QPushButton(title)
			vbox_related.addWidget(btn)
			btn.clicked.connect(related_clicked(href))
			btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		widget_related = QWidget()
		widget_related.setLayout(vbox_related)
		widget_related.setMaximumWidth(240)
		self.related_defs_scroll_area.setWidget(widget_related)
	
	def viewSavedSenses(self):
		table = '<table border="1">'
		for i in self.saved_senses:
			table += "<tr><td>" + i.get_word_html() + "</td><td>" + i.get_def_html() + "</td></tr>"
		table += "</table>"
		# pg = QWebPage()
		# pg.mainFrame().setHtml(table)
		wk = QTextEdit()
		wk.setHtml(table)
		print wk.focusPolicy()
		wk.setFocusPolicy(Qt.ClickFocus)
		self.scroll_area.setWidget(wk)
		# right panel:
		right_panel_l = QVBoxLayout()
		edit_btn = QPushButton("EDIT (UNIMPLEMENTED)")
		def edit_button_pressed():
			pass #TODO
		right_panel_l.addWidget(edit_btn)
		right_panel = QWidget()
		right_panel.setLayout(right_panel_l)
		self.related_defs_scroll_area.setWidget(right_panel)
	
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
