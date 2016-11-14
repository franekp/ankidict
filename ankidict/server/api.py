# -*- coding: utf-8 -*-

import os
import json
import functools

from PyQt4 import QtCore
import cherrypy

from addon.main_thread_executor import executes_in_main_thread

from libdict import macmillan
import aqt


def apiview(func):
    @functools.wraps(func)
    @cherrypy.expose
    @executes_in_main_thread
    def newfunc(*args, **kwargs):
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(func(*args, **kwargs))
    return newfunc


class Reviewer(object):
    def __init__(self, reviewer_obj):
        self.reviewer_obj = reviewer_obj

    def get_card(self):
        if self.reviewer_obj.is_finished():
            return dict(finished=True)
        else:
            btns = self.reviewer_obj.buttons()
            invls = self.reviewer_obj.intervals()
            buttons = [
                dict(button=btn, interval=invls[btn])
                for btn in btns
            ]
            card = dict(
                question=self.reviewer_obj.get_question(),
                answer=self.reviewer_obj.get_answer(),
            )
            remaining = self.reviewer_obj.remaining()
            return dict(
                finished=False,
                buttons=buttons,
                card=card,
                remaining=remaining,
            )

    @apiview
    def index(self, deckid, answer=None):
        self.reviewer_obj.select_deck_by_id(int(deckid))
        if answer is not None:
            assert answer in ['again', 'hard', 'good', 'easy']
            self.reviewer_obj.answer_card(answer)
        return self.get_card()


@cherrypy.popargs('deckid')
class Decks(object):
    def __init__(self, reviewer_obj):
        self.reviewer_obj = reviewer_obj
        self.reviewer = Reviewer(reviewer_obj)

    @apiview
    def index(self):
        return self.reviewer_obj.list_decks()


class AnkiDictApi(object):
    def __init__(self, reviewer_obj):
        self.decks = Decks(reviewer_obj)

    @apiview
    def close(self):
        aqt.mw.ankidict.deactivate_reviews()
        return None

    @apiview
    def dictionary(self, word):
        res = macmillan.query_site(word, plain_dict=True)
        return res
