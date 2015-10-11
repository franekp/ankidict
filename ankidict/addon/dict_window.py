# -*- coding: utf-8 -*-

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from addon import collection
from libdict import macmillan
import re
import datetime
from addon.collection import get_plugin
from addon import basegui

# TODO LIST:

# - (edit mode) in the word list [DONE]
# - add senses folding to UI [DONE]
# - adding examples to the wordlist (and appropriate config entry for it)  [DONE]
# - add intro_paragraph to UI [DONE]
# - global word list to files (named by each month) [DONE]
# - change "related" stuff from buttons to labels (for proper word wrap and space saving) [DONE]
# - add proper special searches handling (:start, :l, etc.)


# TODO:


# - caching entries in a db!
# - downloading related links ahead of time when entry was loaded IMPORTANT!!!
# - autocomplete - lol
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


def tostr(a):
    if a is None:
        return ""
    else:
        return a


class DictWindow(basegui.DictWindow):
    
    def __init__(self):
        super(DictWindow, self).__init__()
        self.init_begin()
        
        self.welcome_view = WelcomeView()
        self.wordlist_view = WordListView()
        self.settings_view = SettingsView()
        
        self.search_input.returnPressed.connect(self.dictSearchEvent)
        self.search_button.clicked.connect(self.dictSearchEvent)
        self.prev_button.clicked.connect(self.prevView)
        self.next_button.clicked.connect(self.nextView)
        self.wordlist_button.clicked.connect(lambda: self.setView(self.wordlist_view))
        self.settings_button.clicked.connect(lambda: self.setView(self.settings_view))
        
        # after pressing prev_button:
        self.prev_views = []
        # after pressing next_button:
        self.next_views = []
        # what is now displayed:
        self.current_view = self.welcome_view

        self.init_end()

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
    
    def makeView(self, s):
        res = macmillan.query_site(s)
        return DictEntryView(res)
    
    def dictSearchEvent(self):
        self.setView(self.makeView(self.search_input.text()))
    
    def dictSearch(self, query):
        self.setView(self.makeView(query))


class BaseView(object):
    def __init__(self):
        super(BaseView, self).__init__()
    # returns what should be placed in the search_input textbox
    def getTitle(self):
        raise "BaseView is an abstract class!"
    # if True, then every appearance of it will be saved into the history of searches
    def isHistRecorded(self):
        raise "BaseView is an abstract class!"


class WelcomeView(BaseView, QWidget):
    def __init__(self):
        super(WelcomeView, self).__init__()
        self.main_vbox = QVBoxLayout()
        self.main_vbox.addWidget(QLabel("Welcome to our addon!"))
        self.setLayout(self.main_vbox)
    def getTitle(self):
        return ""
    def isHistRecorded(self):
        return True


class WordListView(BaseView, QWidget):
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
        tr = "<tr><td>" + sense.original_key + "</td><td>" + sense.definition + "</td></tr>"
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
        return ""
    def isHistRecorded(self):
        return False


class SettingsView(BaseView, QWidget):
    def __init__(self):
        super(SettingsView, self).__init__()
        self.main_vbox = QVBoxLayout()
        self.main_vbox.addWidget(QLabel("SettingsView"))
        self.setLayout(self.main_vbox)
        pass
    def getTitle(self):
        return ""
    def isHistRecorded(self):
        return False


class DictEntryView(BaseView, basegui.DictEntryView):
    def __init__(self, entry):
        super(DictEntryView, self).__init__()
        self.dwnd = get_plugin().dwnd
        self.entry = entry
        # self.examples_widget is required for superclass __init__
        self.examples_widget = ExamplesWidget(self)
        self.init_begin()
        
        for i in entry.senses:
            self.add_sense_widget(SenseWidget(i, self))
        
        for link in entry.links:
            # TODO change it to use 'Destination' object
            # tej lambdy NIE można uprościć, bo inaczej się zbuguje:
            self.add_link(link, (lambda t: lambda: get_plugin().dwnd.dictSearch(t))(link.url) )
        
        self.init_end()

    def getTitle(self):
        return self.entry.original_key
    def isHistRecorded(self):
        return True


class SenseWidget(basegui.SenseWidget):
    def __init__(self, sense, entry_view):
        super(SenseWidget, self).__init__()
        self.sense = sense
        self.entry_view = entry_view
        self.dwnd = get_plugin().dwnd
        self.init_begin()
        
        self.add_btn.clicked.connect(self.saveDef)
        
        for example in sense.examples:
            def add_ex_func(k,e):
                def f():
                    self.entry_view.examples_widget.addExample(k, e)
                    self.entry_view.dwnd.wordlist_view.addExample(k, e, entry_view.entry.original_key)
                return f
            self.add_example(example, add_ex_func(example.original_key, example.content))
        
        self.init_end()
    
    # in the settings should be whether to hide the examples or not
    def leaveEvent(self, event):
        self.hidden_examples.onLeaveEvent(event)
    
    def saveDef(self):
        self.dwnd.wordlist_view.addSense(self.sense)
        collection.add_note(self.format_key_html(), self.format_erased_definition_html())


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
        k = "____".join(k.split(self.entry_view.entry.original_key))
        e = "____".join(e.split(self.entry_view.entry.original_key))
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
        collection.add_note(q, "<strong>"+self.entry_view.entry.original_key+"</strong>")
        for i in self.examples:
            i.hide()
        self.examples = []
        self.add_button.hide()
        
