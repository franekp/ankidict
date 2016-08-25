# -*- coding: utf-8 -*-

####
# Copyright (c) 2014 Wojciech Kordalski
# Copyright (c) 2014 Franciszek Piszcz
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

import sys

from aqt import mw
import aqt
from aqt.qt import *
from PyQt4 import QtCore
import cherrypy

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
        self.initialized_dictionary = False
        self.initialized_reviews = False

        from addon.collection import Collection
        from addon.reviewer import Reviewer
        self.col = Collection()
        self.reviewer = Reviewer()

        # place where we want to place our menu action
        basep = mw.form.menuTools.actions()[6]

        mw.form.menuTools.insertSeparator(basep)

        self.dictact = QAction("AnkiDict: Macmillan dictionary", mw)
        self.dictact.setShortcut("Ctrl+D")
        mw.connect(self.dictact, SIGNAL("triggered()"), self.show_dictionary)
        mw.form.menuTools.insertAction(basep, self.dictact)

        self.reviewact = QAction("AnkiDict: Review cards", mw)
        self.reviewact.setShortcut("Ctrl+R")
        mw.connect(self.reviewact, SIGNAL("triggered()"), self.show_reviews)
        mw.form.menuTools.insertAction(basep, self.reviewact)
        self.init_webserver()
        QtCore.QTimer.singleShot(
            100,
            lambda: self.init_reviews()
        )

    def init_dictionary(self):
        """
        Initializes the dictionary engine if needed.
        Loads some files, etc.
        If called before, does nothing.
        """
        if self.initialized_dictionary:
            return
        # here can be some initialization
        # return False to say: "Initialization failed"
        from addon.gui import DictWindow
        self.dwnd = DictWindow()
        self.initialized_dictionary = True
        self.open_destination("make")
        self.dwnd.hide()

    def init_webserver(self):
        aqt.mw.app.aboutToQuit.connect(cherrypy.engine.exit)
        cherrypy.config.update({'server.socket_port': 9090})
        cherrypy.log.screen = False
        del cherrypy._cpchecker.Checker.check_skipped_app_config
        cherrypy.engine.autoreload.unsubscribe()
        #cherrypy.quickstart(MyServer())
        from addon.myserver import MyServer
        cherrypy.tree.mount(MyServer(self.reviewer))
        cherrypy.engine.start()

    def init_reviews(self):
        if self.initialized_reviews:
            return
        self.reviewer.init()
        from addon.review_view import ReviewView
        self.review_view = ReviewView(
            daily_review_time=self.config.daily_review_time,
            poll_interval_seconds=self.config.poll_interval_seconds,
        )
        self.initialized_reviews = True
        self.review_view.hide()

    def show_dictionary(self):
        """
        Opens dictionary main window.
        """
        self.init_dictionary()
        self.dwnd.show()

    def show_reviews(self):
        self.init_reviews()
        self.review_view.activate()

    def deactivate_reviews(self):
        self.review_view.deactivate()

    def add_note_example(self, ex):
        note = ex.create_anki_note()
        self.col.add_note(*note,
                          deckname=self.get_user_selected_deck())
        self.dwnd.wordlist_view.add_table_row(*reversed(note))

    def create_user_example(self, sense, ex_text):
        Example = sense.example_class
        ex = Example(
            content=ex_text,
            sense=sense,
        )
        return ex

    def get_user_selected_deck(self):
        """Return selected (in the DictWindow) deck's name."""
        return self.dwnd.select_deck_combobox.currentText()

    def get_deck_names(self):
        return self.col.get_deck_names()

    '''
    def restore_from_file(self):
        with open("anki-crash-restore.html") as f:
            html_txt = f.read()
        from pagemodel.bsoup import PageModel
        from pagemodel.html import Html, Node, Text
        class Restore(PageModel):
            model_class = dict
            page_tree = Html(
                Node.list("tr")(
                    Node.list("td")(
                        content=Text()
                    )
                )
            )
        res = Restore(html_txt)
        res = res['content']
        res = [(k, v.replace("(", "<br><span style='color: grey;'>(") + "</span>")for (k, v) in res]
        for (k, v) in res:
            self.col.add_note(v, k,
                          deckname=self.get_user_selected_deck())
        print(res)
    '''

    def open_destination(self, dest):
        """If dest is a string, open a search for it in a dictionary,
        else if it is a Link model instance, open its destination.
        """
        if isinstance(dest, basestring):
            self.dwnd.load_entry(macmillan.query_site(dest))
        else:
            self.dwnd.load_entry(macmillan.query_site(dest.url))
