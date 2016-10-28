# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore
import cherrypy
from cherrypy.lib.static import serve_file

import aqt
from server.api import AnkiDictApi


class AnkiDictServer(object):
    THISDIR = os.path.dirname(__file__)
    def __init__(self, reviewer):
        self.api = AnkiDictApi(reviewer)

    @cherrypy.expose
    def normalize_css(self):
        path = os.path.join(self.THISDIR, "css", "normalize.css")
        return serve_file(path, content_type="text/javascript")

    @cherrypy.expose
    def style_css(self):
        path = os.path.join(self.THISDIR, "css", "style.css")
        return serve_file(path, content_type="text/css")

    @cherrypy.expose
    def index(self):
        path = os.path.join(self.THISDIR, "index.html")
        return (
            i.replace("<%", "").replace("%>", "")
            for i in
            serve_file(path, content_type="text/html")
        )

    @cherrypy.expose
    def elmapp_js(self):
        path = os.path.join(self.THISDIR, "elmapp", "main.js")
        return serve_file(path, content_type="text/javascript")
