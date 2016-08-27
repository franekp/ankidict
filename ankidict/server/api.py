# -*- coding: utf-8 -*-

import os
import json
import functools

from PyQt4 import QtCore
import cherrypy

from addon.main_thread_executor import executes_in_main_thread
import aqt


def apiview(func):
    @functools.wraps(func)
    @cherrypy.expose
    @executes_in_main_thread
    def newfunc(*args, **kwargs):
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(func(*args, **kwargs))
    return newfunc


class AnkiDictApi(object):
    def __init__(self, reviewer):
        self.reviewer = reviewer

    @apiview
    def card(self):
        if self.reviewer.is_finished():
            return dict(
                finished=True,
                deck=self.reviewer.current_deck(),
            )
        else:
            return dict(
                question=self.reviewer.get_question(),
                answer=self.reviewer.get_answer(),
                deck=self.reviewer.current_deck(),
            )

    @apiview
    def remaining(self):
        return self.reviewer.remaining()

    @cherrypy.expose
    @executes_in_main_thread
    def deactivate(self):
        aqt.mw.ankidict.deactivate_reviews()
        return "OK"

    @cherrypy.expose
    @executes_in_main_thread
    def again(self):
        self.reviewer.answer_card('again')
        return "OK"

    @cherrypy.expose
    @executes_in_main_thread
    def hard(self):
        self.reviewer.answer_card('hard')
        return "OK"

    @cherrypy.expose
    @executes_in_main_thread
    def good(self):
        self.reviewer.answer_card('good')
        return "OK"

    @cherrypy.expose
    @executes_in_main_thread
    def easy(self):
        self.reviewer.answer_card('easy')
        return "OK"

    @apiview
    def buttons(self):
        return self.reviewer.buttons()

    @apiview
    def intervals(self):
        return self.reviewer.intervals()
