# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore
import cherrypy
from cherrypy.lib.static import serve_file

from addon.main import get_plugin
from addon.main_thread_executor import executes_in_main_thread
import aqt


# docelowo API będzie potrzebować executes_in_main_thread ale
# pliki statyczne nie będą tego potrzebować

class AnkiDictServer(object):
    THIRDPARTY = os.path.join(os.path.dirname(__file__), "thirdparty")
    THISDIR = os.path.dirname(__file__)
    def __init__(self, reviewer):
        self.reviewer = reviewer

    @cherrypy.expose
    def jquery_js(self):
        path = os.path.join(self.THIRDPARTY, "jquery.js")
        return serve_file(path, content_type="text/javascript")

    @cherrypy.expose
    def normalize_css(self):
        path = os.path.join(self.THIRDPARTY, "normalize.css")
        return serve_file(path, content_type="text/javascript")

    @cherrypy.expose
    def style_css(self):
        path = os.path.join(self.THISDIR, "style.css")
        return serve_file(path, content_type="text/css")

    @cherrypy.expose
    def index(self):
        path = os.path.join(self.THISDIR, "review.html")
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
