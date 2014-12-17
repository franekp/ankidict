# -*- coding: utf-8 -*-

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
import macm_parser_css
import collection

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
class DictWindowOld(QtGui.QWidget):

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
				btn.clicked.connect(results_element_clicked(title))
			widget_results = QWidget()
			widget_results.setLayout(vbox_results)
			self.scroll_area.setWidget(widget_results)
			return
		
		# senses definitions and phrases:
		flayout_senses = QtGui.QVBoxLayout()
		def save_sense(i):
			def tmp():
				self.saved_senses += [i]
				collection.add_note(i.get_def_html(), i.get_word_html())
			return tmp
		d_entry_all = dict_entry.senses + dict_entry.phrases
		for i in d_entry_all:
			wk = QtWebKit.QWebView()
			wk.setHtml(i.get_html())
			btn = QtGui.QPushButton("ADD")
			
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


class DictWindow(QtGui.QWidget):
	
	def __init__(self):
		super(DictWindow, self).__init__()
		self.search_input = QLineEdit(":welcome")
		self.search_button = QPushButton("SEARCH")
		self.prev_button = QPushButton("<|")
		self.next_button = QPushButton("|>")
		self.prev_button.setEnabled(False)
		self.next_button.setEnabled(False)
		self.wordlist_button = QPushButton("LIST")
		self.settings_button = QPushButton("=C")
		
		self.welcome_view = WelcomeView()
		self.wordlist_view = WordListView()
		self.settings_view = SettingsView()
		
		self.search_input.returnPressed.connect(self.dictSearchEvent)
		self.search_button.clicked.connect(self.dictSearchEvent)
		self.prev_button.clicked.connect(self.prevView)
		self.next_button.clicked.connect(self.nextView)
		self.wordlist_button.clicked.connect(lambda : self.setView(self.wordlist_view))
		self.settings_button.clicked.connect(lambda : self.setView(self.settings_view))
		
		# after pressing prev_button:
		self.prev_views = []
		# after pressing next_button:
		self.next_views = []
		# what is now displayed:
		self.current_view = self.welcome_view
		self.head_hbox = QHBoxLayout()
		self.head_hbox.addWidget(self.prev_button)
		self.head_hbox.addWidget(self.next_button)
		self.head_hbox.addWidget(self.search_input)
		self.head_hbox.addWidget(self.search_button)
		self.head_hbox.addWidget(self.wordlist_button)
		self.head_hbox.addWidget(self.settings_button)
		self.main_vbox = QVBoxLayout()
		self.main_vbox.addLayout(self.head_hbox)
		self.main_vbox.addWidget(self.current_view)
		self.setLayout(self.main_vbox)
		self.resize(800,600)
		self.setWindowTitle('Macmillan Dictionary')
		
		self.view_factory = ViewFactory(self)
		
		self.dictSearch("make")
	
	def __updatePrevNextBtns(self):
		self.prev_button.setEnabled(self.prev_views != [])
		self.next_button.setEnabled(self.next_views != [])
	
	def setView(self, v):
		if v == None:
			return
		self.search_input.setText(v.getTitle())
		if self.current_view.isHistRecorded():
			self.prev_views.append(self.current_view)
		self.current_view.hide()
		self.current_view = v
		self.main_vbox.addWidget(v)
		v.show()
		self.__updatePrevNextBtns()
	
	def prevView(self):
		if self.prev_views == []:
			print "ERROR: no more prev_views!"
			return
		self.next_views.append(self.current_view)
		self.current_view.hide()
		self.current_view = self.prev_views[-1]
		self.prev_views = self.prev_views[:-1]
		self.current_view.show()
		self.search_input.setText(self.current_view.getTitle())
		self.__updatePrevNextBtns()
	
	def nextView(self):
		if self.next_views == []:
			print "ERROR: no more next_views!"
			return
		self.prev_views.append(self.current_view)
		self.current_view.hide()
		self.current_view = self.next_views[-1]
		self.next_views = self.next_views[:-1]
		self.current_view.show()
		self.search_input.setText(self.current_view.getTitle())
		self.__updatePrevNextBtns()
	
	def closeEvent(self, event):
		event.ignore()
		self.hide()
	
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			# Selecting the search input field
			self.search_input.setFocus()
			self.search_input.setText("")
	
	def dictSearchEvent(self):
		self.setView(self.view_factory.makeView(self.search_input.text()))
	
	def dictSearch(self, query):
		self.setView(self.view_factory.makeView(query))

class ViewFactory(object):
	''' here goes caching of dict entries, interpreting user commands, etc. '''
	def __init__(self, dwnd):
		self.dwnd = dwnd
	
	def makeView(self, s):
		res = macm_parser_css.dict_query(s)
		if isinstance(res, macm_parser_css.DictEntry):
			return DictEntryView(res, self.dwnd)
		else:
			return WelcomeView()

class BaseView(QWidget):
	def __init__(self):
		super(BaseView, self).__init__()
	# returns what should be placed in the search_input textbox
	def getTitle(self):
		raise "BaseView is an abstract class!"
	# if True, then every appearance of it will be saved into the history of searches
	def isHistRecorded(self):
		raise "BaseView is an abstract class!"
	
	pass

class WelcomeView(BaseView):
	def __init__(self):
		super(WelcomeView, self).__init__()
		self.main_vbox = QVBoxLayout()
		self.main_vbox.addWidget(QLabel("Welcome to our addon!"))
		self.setLayout(self.main_vbox)
	def getTitle(self):
		return ":welcome"
	def isHistRecorded(self):
		return True


class SearchResultsView(BaseView):
	pass

class WordListView(BaseView):
	def __init__(self):
		super(WordListView, self).__init__()
		self.main_vbox = QVBoxLayout()
		self.main_vbox.addWidget(QLabel("WordListView"))
		self.setLayout(self.main_vbox)
		pass
	
	def addWord(self):
		pass
	
	def getTitle(self):
		return ":l"
	def isHistRecorded(self):
		return True

class SettingsView(BaseView):
	def __init__(self):
		super(SettingsView, self).__init__()
		self.main_vbox = QVBoxLayout()
		self.main_vbox.addWidget(QLabel("SettingsView"))
		self.setLayout(self.main_vbox)
		pass
	def getTitle(self):
		return ":s"
	def isHistRecorded(self):
		return True


class DictEntryView(BaseView):
	def __init__(self, entry, dwnd):
		super(DictEntryView, self).__init__()
		self.entry = entry
		self.dwnd = dwnd
		left_scroll = QScrollArea()
		right_scroll = QScrollArea()
		left_widget = QWidget()
		right_widget = QWidget()
		self.left_vbox = QVBoxLayout()
		self.right_vbox = QVBoxLayout()
		self.main_hbox = QHBoxLayout()
		
		entry_all = entry.senses + entry.phrases
		for i in entry_all:
			self.left_vbox.addWidget(SenseWidget(i, self))
		for (title, href) in entry.related:
			btn = QPushButton(title)
			# tej lambdy NIE można uprościć, bo inaczej się zbuguje:
			btn.clicked.connect( (lambda t: lambda: dwnd.dictSearch(t))(href) )
			self.right_vbox.addWidget(btn)
		
		#left_scroll.setLayout(self.left_vbox)
		#right_scroll.setLayout(self.right_vbox)
		left_scroll.setWidgetResizable(True)
		right_scroll.setWidgetResizable(True)
		left_widget.setLayout(self.left_vbox)
		right_widget.setLayout(self.right_vbox)
		left_widget.show()
		right_widget.show()
		left_scroll.setWidget(left_widget)
		right_scroll.setWidget(right_widget)
		right_scroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.main_hbox.addWidget(left_scroll)
		self.main_hbox.addWidget(right_scroll)
		self.setLayout(self.main_hbox)
		
	def getTitle(self):
		#FIXME
		return "sth"
	def isHistRecorded(self):
		return True

class SenseWidget(QWidget):
	def __init__(self, sense, entry_view):
		super(SenseWidget, self).__init__()
		self.sense = sense
		self.entry_view = entry_view
		self.dwnd = entry_view.dwnd
		self.main_vbox = QVBoxLayout()
		self.def_hbox = QHBoxLayout()
		
		self.main_vbox.setMargin(0)
		self.def_hbox.setMargin(0)
		self.main_vbox.setSpacing(0)
		self.def_hbox.setSpacing(0)
		
		tmplabel = QLabel(sense.get_word_html() + "  ---  " + sense.get_full_def_html())
		tmplabel.setWordWrap(True)
		tmplabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
		#tmplabel.setScaledContents(True)
		tmplabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		
		self.def_hbox.addWidget(tmplabel)
		btn = QPushButton("ADD")
		btn.clicked.connect(self.save_def)
		self.def_hbox.addWidget(btn)
		self.main_vbox.addLayout(self.def_hbox)
		for (key, ex) in sense.examples:
			tmp = '<font color="blue"><i>'
			if key:
				tmp += "<b>"+key+" </b>"
			tmp += ex
			tmp += "</i></font>"
			tmplabel = QLabel(tmp)
			tmplabel.setWordWrap(True)
			tmplabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
			tmplabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
			
			self.main_vbox.addWidget(tmplabel)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
		
		
		self.setLayout(self.main_vbox)
		#self.setStyleSheet("background-color:white;")
		self.setStyleSheet("#sense-widget{border-color:black; border-width: 3px; border-style: double;}")
		self.setObjectName("sense-widget")
		
	def save_def(self):
		pass
	
