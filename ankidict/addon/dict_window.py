# -*- coding: utf-8 -*-

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from addon import macm_parser_css
from addon import collection
import re
import datetime
from addon.collection import get_plugin

# TODO LIST:

# - (edit mode) in the word list [DONE]
# - add senses folding to UI [DONE]
# - adding examples to the wordlist (and appropriate config entry for it)  [DONE]
# - add intro_paragraph to UI [DONE]
# - global word list to files (named by each month) [DONE]
# - change "related" stuff from buttons to labels (for proper word wrap and space saving) [DONE]
# - add proper special searches handling (:start, :l, etc.)


# TODO:

# - add proper closing of word list log file

# - add better key phrase removal from the definitions (e.g. remove also words with 's'/'ed' at the end or phrasal verbs)
#		encapsulate it in separate class/module/whatever and replace existing code with it
# - add special handling of cases where there is only one example added (some list of possible answers)
#		put this in the same module/class that the above
# - add many behavior specifiers to config (and maybe settings view to change the config)
# - add the additional textbox to paste currently studied text (for examples) and textbox with link to it (for additional field in note)
# - add option to add to deck two/more senses as one sense (and think how to do it sensibly in the UI)
#   (or maybe do it at the deck level - utility to merge the cards with the same key)
# - utility for learning synonyms - some form of grouping thgs.
# - make usable distribution so that people can install it easily (best option - through Anki addon-manager)
# - POSSIBLE IDEA : maybe write something such as a 'scraper generator' - generating scrapers from unit tests for them - this can be interesting thing...
#    (this is good as long as content is not changing, but website code may change)
# - scraping unit tests... - launched automatically for ex. every month

# windows utilities...

# main dictionary window


class DictWindow(QtGui.QWidget):
	
	def __init__(self):
		super(DictWindow, self).__init__()
		def conf_btn(btn):
			btn.setMaximumWidth(60)
			btn.setStyleSheet("font-weight: bold; font-family: monospace")
		self.search_input = QLineEdit(":welcome")
		self.search_button = QPushButton("SEARCH")
		self.prev_button = QPushButton("<-")
		self.next_button = QPushButton("->")
		self.prev_button.setEnabled(False)
		self.next_button.setEnabled(False)
		self.prev_button.setMaximumWidth(66)
		self.next_button.setMaximumWidth(66)
		self.wordlist_button = QPushButton("LIST")
		self.settings_button = QPushButton("==C")
		conf_btn(self.prev_button)
		conf_btn(self.next_button)
		#conf_btn(self.search_button)
		#conf_btn(self.wordlist_button)
		conf_btn(self.settings_button)
		
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
		
		#self.dictSearch("make")
	
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
		if self.current_view.isHistRecorded():
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
		if self.current_view.isHistRecorded():
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
		if s == ":start" or s == ":help" or s == ":h":
			return self.dwnd.welcome_view
		if s == ":l":
			return self.dwnd.wordlist_view
		if s == ":s":
			return self.dwnd.settings_view
		res = macm_parser_css.dict_query(s)
		if isinstance(res, macm_parser_css.DictEntry):
			return DictEntryView(res, self.dwnd)
		else:
			return SearchResultsView(res, self.dwnd)

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
		return ":start"
	def isHistRecorded(self):
		return True

class WordListView(BaseView):
	def __init__(self):
		super(WordListView, self).__init__()
		self.main_hbox = QHBoxLayout()
		self.text_edit = QTextEdit()
		self.text_edit.setHtml('<table border="2" style="border-color: black; border-width: 2; border-style: solid;"> </table>')
		self.main_hbox.addWidget(self.text_edit)
		self.setLayout(self.main_hbox)
		def func_constr(f):
			def wyn(e):
				f(e)
				if e.key() == QtCore.Qt.Key_Backspace:
					self.reloadTable()
			return wyn
		self.text_edit.keyPressEvent = func_constr(self.text_edit.keyPressEvent)
		if get_plugin().config.log_wordlist:
			today = datetime.date.today()
			filename = "millandict_wordlist_log_"+str(today.month) + "_" +str(today.year) + ".html"
			self.logfile = open(filename, "a+")
		
	
	def addSense(self, sense):
		tr = "<tr><td>" + sense.get_word_html() + "</td><td>" + sense.get_def_html() + "</td></tr>"
		text = self.text_edit.toHtml()[:-(len("</table></body></html>"))] + tr + "</table></body></html>"
		text = 'border="2"'.join(text.split('border="0"'))
		self.text_edit.setHtml(text)
		if get_plugin().config.log_wordlist:
			self.logfile.write(tr.encode("ascii","ignore") + "\n")
		#print self.text_edit.toHtml()
	
	def addExample(self, k, e, word):
		if not (get_plugin().config.add_examples_to_list):
			return
		if k == "":
			k = word
		tr = "<tr><td>" + k + "</td><td>" + "____".join(e.split(word)) + "</td></tr>"
		text = self.text_edit.toHtml()[:-(len("</table></body></html>"))] + tr + "</table></body></html>"
		text = 'border="2"'.join(text.split('border="0"'))
		self.text_edit.setHtml(text)
		if get_plugin().config.log_wordlist:
			self.logfile.write(tr.encode("ascii","ignore") + "\n")
	
	def reloadTable(self):
		text = self.text_edit.toHtml()
		text = 'border="2"'.join(text.split('border="0"'))
		#text = ''.join(text.split('<td></td>'))
		text = ''.join(re.split(r'<tr>\s*<td>\s*</td>\s*<td>\s*</td>\s*</tr>',text))
		#print text
		cursor = self.text_edit.textCursor()
		c_pos = self.text_edit.cursorRect().center()
		self.text_edit.setHtml(text)
		self.text_edit.setTextCursor(self.text_edit.cursorForPosition(c_pos))
	
	def getTitle(self):
		return ":l"
	def isHistRecorded(self):
		return False
		

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
		return False


class SearchResultsView(BaseView):
	def __init__(self, results, dwnd):
		super(SearchResultsView, self).__init__()
		self.results = results
		self.main_vbox = QVBoxLayout()
		for i in results.results:
			lab = QLabel("<h3><a href='"+i+"'>"+i+"</a></h3>")
			# tej lambdy NIE można uprościć, bo inaczej się zbuguje:
			lab.linkActivated.connect((lambda t: lambda: dwnd.dictSearch(t))(i))
			
			lab.setAlignment(Qt.AlignHCenter)
			self.main_vbox.addWidget(lab)
		self.setLayout(self.main_vbox)
	def getTitle(self):
		return self.results.word
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
		self.examples_widget = ExamplesWidget(self)
		entry_all = entry.intro_paragraph_sense_l + entry.senses + entry.phrases
		for i in entry_all:
			self.left_vbox.addWidget(SenseWidget(i, self))
		
		for (title, href) in entry.related:
			btn = QLabel('<a href="related" style="text-decoration: none; color: black;"><strong>' + title + "</strong></a>")
			# tej lambdy NIE można uprościć, bo inaczej się zbuguje:
			btn.linkActivated.connect( (lambda t: lambda: dwnd.dictSearch(t))(href) )
			btn.show()
			btn.setWordWrap(True)
			def make_line():
				fr = QFrame()
				#fr.setStyleSheet("background-color: white;");
				fr.setFrameShape(QFrame.HLine)
				fr.setFrameShadow(QFrame.Sunken)
				fr.setLineWidth(2)
				#fr.setMidLineWidth(1)
				return fr
			self.right_vbox.addWidget(btn)
			self.right_vbox.addWidget(make_line())
		
		left_scroll.setWidgetResizable(True)
		right_scroll.setWidgetResizable(True)
		left_widget.setLayout(self.left_vbox)
		right_widget.setLayout(self.right_vbox)
		left_widget.show()
		right_widget.show()
		left_scroll.setWidget(left_widget)
		right_scroll.setWidget(right_widget)
		right_scroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		# TODO: potem i tak to będą jakieś labelsy, więc się będą zawijać i będzie dobrze
		right_scroll.setMaximumWidth(get_plugin().config.related_defs_panel_width)
		left_column = QVBoxLayout()
		left_column.addWidget(left_scroll)
		left_column.addWidget(self.examples_widget)
		self.main_hbox.addLayout(left_column)
		self.main_hbox.addWidget(right_scroll)
		self.setLayout(self.main_hbox)
		
	def getTitle(self):
		return self.entry.word
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
		
		self.main_vbox.addWidget(tmplabel)
		btn = QPushButton("ADD")
		btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		btn.clicked.connect(self.saveDef)
		
		self.examples_to_hide = []
		
		#self.main_vbox.addLayout(self.def_hbox)
		for (key, ex) in sense.examples:
			tmp = '<a href="example" style="'+get_plugin().config.example_style+'"><i>'
			if key:
				tmp += "<b>"+key+" </b>"
			tmp += ex
			tmp += "</i></a>"
			tmplabel = QLabel(tmp)
			tmplabel.setWordWrap(True)
			tmplabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
			tmplabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
			def add_ex_func(k,e):
				def f():
					self.entry_view.examples_widget.addExample(k, e)
					self.entry_view.dwnd.wordlist_view.addExample(k, e, entry_view.entry.word)
				return f
			tmplabel.linkActivated.connect(add_ex_func(key, ex))
			self.examples_to_hide.append(tmplabel)
		self.examples_all = self.examples_to_hide
		self.examples_to_hide = self.examples_to_hide[(get_plugin().config.max_examples_per_sense):]
		
		def make_frame():
			fr = QFrame()
			fr.setStyleSheet("background-color: white;");
			fr.setFrameShape(QFrame.Box)
			fr.setFrameShadow(QFrame.Raised)
			fr.setLineWidth(2)
			fr.setMidLineWidth(2)
			return fr
		def make_hidden_examples():
			w = QWidget()
			w.onLeaveEvent = lambda e: None
			if self.examples_all == []:
				return w
			w.setMouseTracking(True)
			lab = QLabel('<a href="example" style="'+get_plugin().config.example_style+'"><b> ... ... ... </b></a>')
			lab.hide()
			layout = QVBoxLayout()
			for i in self.examples_all:
				layout.addWidget(i)
			layout.setMargin(2)
			layout.addWidget(lab)
			w.setLayout(layout)
			def onEnterEvent(event):
				# here showing examples (takie onHover)
				for i in self.examples_to_hide:
					i.show()
				lab.hide()
			def onLeaveEvent(event):
				# here hiding examples (takie onUnHover)
				for i in self.examples_to_hide:
					i.hide()
				if self.examples_to_hide != []:
					lab.show()
			def mouseMoveEvent(event):
				if event.x() < get_plugin().config.examples_hover_area_width :
					onEnterEvent(event)
				else:
					onLeaveEvent(event)
			#w.enterEvent = onEnterEvent
			#w.leaveEvent = onLeaveEvent
			w.mouseMoveEvent = mouseMoveEvent
			w.onLeaveEvent = onLeaveEvent
			w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
			onLeaveEvent(None)
			w.show()
			return w
		self.hidden_examples = make_hidden_examples()
		self.main_vbox.addWidget(self.hidden_examples)
		frame = make_frame()
		frame.setLayout(self.main_vbox)
		self.def_hbox.addWidget(frame)
		self.def_hbox.addWidget(btn)
		
		
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
		
		self.setLayout(self.def_hbox)
	
	# in the settings should be whether to hide the examples or not
	def leaveEvent(self, event):
		self.hidden_examples.onLeaveEvent(event)
	
	def saveDef(self):
		self.dwnd.wordlist_view.addSense(self.sense)
		collection.add_note(self.sense.get_def_html(), self.sense.get_word_html())

class Example(QLabel):
		def __init__(self, txt):
			super(Example, self).__init__('<a href="example" style="'+get_plugin().config.example_style+'">'+txt+'</a>')
			self.txt = txt
		def mouseReleaseEvent(self, e):
			self.txt = ""
			self.hide()

class ExamplesWidget(QWidget):
	
	def __init__(self, entry_view):
		super(ExamplesWidget, self).__init__()
		self.entry_view = entry_view
		self.examples = []
		self.main_hbox = QHBoxLayout()
		self.list_vbox = QVBoxLayout()
		self.main_hbox.addLayout(self.list_vbox)
		self.add_button = QPushButton("ADD")
		self.add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.main_hbox.addWidget(self.add_button)
		self.add_button.hide()
		self.add_button.clicked.connect(self.addToCollection)
		self.setLayout(self.main_hbox)
		#self.addExample("","here should be some examples...")
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
	def addExample(self, k, e):
		k = "____".join(k.split(self.entry_view.entry.word))
		e = "____".join(e.split(self.entry_view.entry.word))
		txt = '<i>'
		if k:
			txt += "<b>"+k+" </b>"
		txt += e
		txt += "</i>"
		ex = Example(txt)
		self.examples.append(ex)
		self.list_vbox.addWidget(ex)
		self.setLayout(self.main_hbox)
		self.add_button.show()
	def mouseReleaseEvent(self, e):
		self.examples = filter((lambda a: a.txt != ""), self.examples)
		if self.examples == []:
			self.add_button.hide()
	def addToCollection(self):
		self.mouseReleaseEvent(None)
		q = "<br />".join(map((lambda a: a.txt), self.examples))
		collection.add_note(q, "<strong>"+self.entry_view.entry.word+"</strong>")
		for i in self.examples:
			i.hide()
		self.examples = []
		self.add_button.hide()
		
