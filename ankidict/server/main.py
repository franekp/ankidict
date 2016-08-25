# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore
import cherrypy
from cherrypy.lib.static import serve_file

import aqt
from server.api import AnkiDictApi


class AnkiDictServer(object):
    THIRDPARTY = os.path.join(os.path.dirname(__file__), "thirdparty")
    THISDIR = os.path.dirname(__file__)
    def __init__(self, reviewer):
        self.api = AnkiDictApi(reviewer)

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

    
