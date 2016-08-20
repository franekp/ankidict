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

import os

from PyQt4 import QtCore
import cherrypy
from cherrypy.lib.static import serve_file

from addon.main import get_plugin
from addon.main_thread_executor import executes_in_main_thread


# docelowo API będzie potrzebować executes_in_main_thread ale
# pliki statyczne nie będą tego potrzebować


class MyServer(object):
    def __init__(self, reviewer):
        self.reviewer = reviewer

    @cherrypy.expose
    def jquery_js(self):
        path = os.path.join(os.path.dirname(__file__), "jquery.js")
        return serve_file(path, content_type="text/javascript")

    @cherrypy.expose
    def style_css(self):
        path = os.path.join(os.path.dirname(__file__), "style.css")
        return serve_file(path, content_type="text/css")

    @cherrypy.expose
    def background_image_jpg(self):
        path = os.path.join(os.path.dirname(__file__), "background.jpg")
        return serve_file(path, content_type="image/jpg")

    @cherrypy.expose
    def index(self):
        path = os.path.join(os.path.dirname(__file__), "review.html")
        return (
            i.replace("<%", "").replace("%>", "")
            for i in
            serve_file(path, content_type="text/html")
        )

    @cherrypy.expose
    @executes_in_main_thread
    def get_question(self):
        return self.reviewer.get_question()

    @cherrypy.expose
    @executes_in_main_thread
    def get_answer(self):
        return self.reviewer.get_answer()

    @cherrypy.expose
    @executes_in_main_thread
    def get_remaining(self):
        return self.reviewer.get_remaining()

    @cherrypy.expose
    @executes_in_main_thread
    def deactivate(self):
        self.reviewer.deactivate()
        return "OK"
    
    @cherrypy.expose
    @executes_in_main_thread
    def again(self):
        self.reviewer.again()
        return "OK"
    
    @cherrypy.expose
    @executes_in_main_thread
    def hard(self):
        self.reviewer.hard()
        return "OK"
    
    @cherrypy.expose
    @executes_in_main_thread
    def good(self):
        self.reviewer.good()
        return "OK"
    
    @cherrypy.expose
    @executes_in_main_thread
    def easy(self):
        self.reviewer.easy()
        return "OK"


class Reviewer(object):
    def start_webserver(self):
        cherrypy.config.update({'server.socket_port': 9090})
        #cherrypy.quickstart(MyServer())
        cherrypy.tree.mount(MyServer(self))
        cherrypy.engine.start()

    def __init__(self, col, popup):
        self.popup = popup
        self.server_thread = None
        self.col = col
        self.card = self.col.sched.getCard()
        self.start_webserver()

    def next_card(self):
        self.card = self.col.sched.getCard()
        if not self.card:
            # deck finished! TODO: view this
            pass
        self.popup.reload()

    def select_deck_by_name(self, dname):
        did = self.col.decks.id(deckname)
        self.col.decks.select(did)
        # this is necessary for change to take effect, without this the
        # scheduler keeps giving cards from previous deck
        self.col.reset()

    def get_question(self):
        if self.card is None:
            return "Finished"
        return self.card.note()[get_plugin().config.note_question]

    def get_answer(self):
        if self.card is None:
            return "Finished"
        return self.card.note()[get_plugin().config.note_answer]

    def answer_button_list(self):
        # NOT USED, kept for reference only
        if self.card is None:
            return ((1, "Again"), (2, "Good"))
        l = ((1, _("Again")),)
        cnt = self.col.sched.answerButtons(self.card)
        if cnt == 2:
            return l + ((2, "Good"),)
        elif cnt == 3:
            return l + ((2, "Good"), (3, "Easy"))
        else:
            return l + ((2, "Hard"), (3, "Good"), (4, "Easy"))

    def answer_card(self, ease):
        if self.card is None:
            self.next_card()
        else:
            self.col.sched.answerCard(self.card, ease)
            self.col.autosave()
            self.next_card()

    def again(self):
        self.answer_card(1)

    def hard(self):
        if self.col.sched.answerButtons(self.card) <= 3:
            self.answer_card(1)
        else:
            # use 'again' if 'hard' not available
            self.answer_card(2)

    def good(self):
        if self.col.sched.answerButtons(self.card) <= 3:
            self.answer_card(2)
        else:
            self.answer_card(3)

    def easy(self):
        if self.col.sched.answerButtons(self.card) <= 3:
            self.answer_card(3)
        else:
            self.answer_card(4)

    def get_remaining(self):
        if not self.col.conf['dueCounts']:
            return ""
        if self.card is None: #self.hadCardQueue:
            # if it's come from the undo queue, don't count it separately
            counts = list(self.col.sched.counts())
            idx = None
        else:
            counts = list(self.col.sched.counts(self.card))
            idx = self.col.sched.countIdx(self.card)
        if idx is not None:
            counts[idx] = "<u>%s</u>" % (counts[idx])
        space = " + "
        ctxt = '<font color="#000099">%s</font>' % counts[0]
        ctxt += space + '<font color="#C35617">%s</font>' % counts[1]
        ctxt += space + '<font color="#007700">%s</font>' % counts[2]
        return ctxt

    def deactivate(self):
        self.popup.deactivate()
