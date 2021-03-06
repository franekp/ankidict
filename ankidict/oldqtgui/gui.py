# -*- coding: utf-8 -*-

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
import re
import datetime
import os

from addon.main import get_plugin
from oldqtgui import basegui

# TODO LIST:

# - (edit mode) in the word list [DONE]
# - add senses folding to UI [DONE]
# - adding examples to the wordlist (and appropriate config entry for it)  [DONE]
# - add intro_paragraph to UI [DONE]
# - global word list to files (named by each month) [DONE]
# - change "related" stuff from buttons to labels (for proper word wrap and space saving) [DONE]
# - add proper special searches handling (:start, :l, etc.)


# TODO:

# - in addition to static questions that don't change, add also dynamic questions,
#   that is - take some corpus, and generate the questions from it, always marking
#   sentences as visited. Always select these corpus entries that are the least
#   visited ones. This way each time user practices, they will be presented with
#   entirely new question that asks for a word they are learning and they will
#   need to think for a while which word to use here so the learning will be more
#   focused on actually using the words and less like remembering random sentences
#   (which is also needed to some extent). If the user does not know the answer, he
#   will later be presented some other sentence. This what counts is that user is
#   required to use every word he is learning in some sentence, NOT to complete all
#   sentences.

# also using paralell corpus we may make questions about translating given sentences and
# check if advanced words were used.

# important sources of bi-lingual corpus:
# - !!! http://opus.lingfil.uu.se/ !!! - OPEN SOURCE PARALELL CORPUS, really good!
# - !!! main.edu.pl !!! and similar CS contests sites, their tasks are translated into English

# less important:
# - download pelcra corpora - the literature one
# - wikipedia
# - bible translation
# - other books translations
# - multilingual news services # take some time
#    - pap.pl - small amount of data
#    - globalvoices.org - good quality, but small amount of data
#    they are poorly structured and usually only some of the articles
#    have their pair in another language, many are just different
# - tekstowo.pl and similar song-translation websites # low-quality
# - subtitles from various movies # medium-quality

# possible source of mono-lingual funny corpus:
# - scp-wiki.pl , scp-wiki.net

# GENERAL IDEA IS THAT SOMEHOW WE NEED TO FORCE THE LEARNER TO BUILD SOME
# SENTENCES WITH THE WORDS HE STUDIED TODAY. SO FIRST WE OBTAIN A LIST OF WORDS
# THAT WERE STUDIED TODAY. THEN WE NEED TO CREATE SOME HINTS (SIMPLE IDEA IS THAT
# THEY ARE WORDS FROM PARALELL CORPUS) THAT WILL LEAD TO THE LEARNER USE THE
# WORDS IN _NEW_ SENTENCES. (IT MAY BE IMPORTANT THAT THE USER WRITES _WHOLE_
# SENTENCE INSTEAD OF FILLING THE BLANKS...)

# - SUBSENSES!
# - PREVENT OUT-OF-MEM CRASHES!
# - send crash reports to the author!
# - catch the value errors in PageModel and throw exceptions with shorter traceback,
#     but include the page structure info in exceptions.
# - caching entries in a db!
# - downloading related links ahead of time when entry was loaded IMPORTANT!!!
# - autocomplete - lol
# - add proper closing of word list log file


# - add many behavior specifiers to config (and maybe settings view to change the config)
# - add the additional textbox to paste currently studied text (for examples) and textbox with link to it (for additional field in note)
# - utility for learning synonyms - some form of grouping thgs.
# - make usable distribution so that people can install it easily (best option - through Anki addon-manager)

# - scraping unit tests... - launched automatically for ex. every week

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
        
        style_filepath = os.path.join(os.path.dirname(__file__), 'qt-style.css')
        
        with open(style_filepath) as f:
            style = f.read()
        
        self.setStyleSheet(style)
        
        self.init_begin()
        
        self.welcome_view = WelcomeView()
        self.wordlist_view = WordListView()
        self.settings_view = SettingsView()

        self.search_input.returnPressed.connect(self.dictSearchEvent)
        self.search_button.clicked.connect(self.dictSearchEvent)
        self.prev_button.clicked.connect(self.prevView)
        self.next_button.clicked.connect(self.nextView)
        self.wordlist_button.clicked.connect(lambda: self.setView(self.wordlist_view))

        # after pressing prev_button:
        self.prev_views = []
        # after pressing next_button:
        self.next_views = []
        # what is now displayed:
        self.current_view = self.welcome_view

        self.init_end()
        self.show()
    
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

    def load_entry(self, entry):
        self.setView(DictEntryView(entry))

    def dictSearchEvent(self):
        get_plugin().open_destination(self.search_input.text())


class BaseView(QWidget):
    def __init__(self):
        super(BaseView, self).__init__()
    # returns what should be placed in the search_input textbox
    def getTitle(self):
        raise "BaseView is an abstract class!"
    # if True, then every appearance of it will be saved into the history of searches
    def isHistRecorded(self):
        raise "BaseView is an abstract class!"


class WelcomeView(BaseView):
    def __init__(self):
        super(WelcomeView, self).__init__()
        self.main_vbox = QVBoxLayout()
        self.main_vbox.addWidget(QLabel("Welcome to our addon!"))
        self.setLayout(self.main_vbox)
    def getTitle(self):
        return ""
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
        return ""
    def isHistRecorded(self):
        return False


class DictEntryView(BaseView, basegui.DictEntryView):
    def __init__(self, entry):
        super(DictEntryView, self).__init__()
        self.dwnd = get_plugin().dwnd
        self.entry = entry
        self.init_begin()
        for sense in entry.senses:
            self.add_sense_widget(SenseWidget(sense, self))
        for link in entry.links:
            # tej lambdy NIE można uprościć, bo inaczej się zbuguje:
            self.add_link(link, (lambda t: lambda: get_plugin().open_destination(t))(link) )
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

        for ex in sense.examples:
            self.add_example(ex)
        self.add_textfield_for_custom_examples()

        self.init_end()


class WordListView(BaseView, basegui.WordListView):
    def __init__(self):
        super(WordListView, self).__init__()
        self.init_begin()
        self.init_end()

    def add_sense(self, sense):
        self.add_table_row(sense.format_key_html(),
            sense.get_erased_definition())

    def add_example(self, ex):
        if not (get_plugin().config.add_examples_to_list):
            return
        k = ex.format_key_html()
        e = "<i>" + ex.get_erased_content() + "</i>"
        self.add_table_row(k, e)

    def getTitle(self):
        return ""

    def isHistRecorded(self):
        return False
