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


class CssGenerator(object):
    def offset_color(self, col, amt):
        usePound = False
        if col[0] == "#":
            col = col[1:]
            usePound = True
        num = int(col,16);
        r = (num >> 16) + amt;
        if (r > 255):
            r = 255
        elif  (r < 0):
            r = 0
        b = ((num >> 8) & 0x00FF) + amt;
        if (b > 255):
            b = 255
        elif (b < 0):
            b = 0
        g = (num & 0x0000FF) + amt;
        if (g > 255):
            g = 255
        elif (g < 0):
            g = 0;
        return ("#" if usePound else "") + "{0:x}".format(g | (b << 8) | (r << 16))

    def get_colors(self):
        colors = """
        #bcd6ef  0%, #a3c1ef  5%, #98b8e9  10%, #91b3e9 15%,
        #8ab1e9 20%, #8ab2ea 25%, #83abe8  30%, #7cabe9 35%,
        #73a6e8 40%, #6ca4e9 45%, #67a1e9  50%, #4693ea 50%,
        #579eec 70%, #64a7ee 75%, #6eaeee  80%, #7db6ef 85%,
        #88bfef 90%, #97caef 95%, #abd4ef 100%
        """.split(",")
        colors = [x.strip().split() for x in colors]
        return colors

    def transform_color(self, c, color, index):
        r = int(c[1:3], 16)
        g = int(c[3:5], 16)
        b = int(c[5:7], 16)
        if color == 'y':
            r, g, b = int(b*1.0), int(g*1.15), r
            return "rgb(%d,%d,%d)" % (r, g, b)
        elif color == 'r':
            r, g, b = b, r, r
            return "rgb(%d,%d,%d)" % (r, g, b)
        elif color == 'g':
            r, g, b = int(r*0.9), int(b*0.8), int(g*0.9)
            return "rgb(%d,%d,%d)" % (r, g, b)
        elif color == 'b':
            # r, g, b = r, b, g
            return "rgb(%d,%d,%d)" % (r, g, b)
        else:
            raise Exception("Wrong argument")

    def make_gradient(self, color):
        col = self.get_colors()
        return [
                (self.transform_color(i[0], color, index), i[1])
                for index, i in enumerate(col)
        ]

    def make_button_style(self, color):
        col = self.make_gradient(color)
        border_color = col[11][0]
        col = ['-90deg'] + [c + " " + p for (c, p) in col]
        grad = "(" + ", ".join(col) + ")"
        res = "{\n"
        res += "border-color: " + border_color + ";\n"
        res += "background: -webkit-linear-gradient" + grad + " !important;\n"
        res += "background-image: -moz-linear-gradient" + grad + " !important;\n"
        res += "}\n"
        return res

    def get_style(self):
        res = ""
        res += ".btn-danger, .btn-danger:hover" + self.make_button_style('r')
        res += ".btn-warning, .btn-warning:hover" + self.make_button_style('y')
        res += ".btn-success, .btn-success:hover" + self.make_button_style('g')
        res += ".btn-primary, .btn-primary:hover" + self.make_button_style('b')
        return res


class MyServer(object):
    def __init__(self, reviewer):
        self.reviewer = reviewer

    @cherrypy.expose
    def bootstrap_theme_css(self):
        path = os.path.join(os.path.dirname(__file__), "green_bootstrap.css")
        res = serve_file(path, content_type="text/css")
        res = "".join(list(res))
        res += CssGenerator().get_style()
        return res

    @cherrypy.expose
    def background_image_jpg(self):
        path = os.path.join(os.path.dirname(__file__), "background.jpg")
        return serve_file(path, content_type="image/jpg")

    @cherrypy.expose
    def index(self):
        path = os.path.join(os.path.dirname(__file__), "review.html")
        return serve_file(path, content_type="text/html")
        

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
