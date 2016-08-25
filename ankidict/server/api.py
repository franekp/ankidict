# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore
import cherrypy

from addon.main_thread_executor import executes_in_main_thread
import aqt


class AnkiDictApi(object):
    def __init__(self, reviewer):
        self.reviewer = reviewer

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
        aqt.mw.ankidict.deactivate_reviews()
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
