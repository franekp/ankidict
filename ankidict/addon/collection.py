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

from aqt import mw
import re

from main import get_plugin

class Collection(object):
    def setup(self):
        self.select_deck()

    def select_deck(self):
        # selects deck
        # [TODO] test
        deckname = get_plugin().config.deck
        deckid = mw.col.decks.id(deckname)

        # select proper model
        self.select_model()

        # choosing deck
        # we need to set it in the model
        m = mw.col.models.current()
        m['did'] = deckid
        mw.col.models.save(m)

    def select_model(self):
        mod = mw.col.models.byName(get_plugin().config.model)
        if not mod:
            # new model is required
            mod = mw.col.models.new(get_plugin().config.model)
            mw.col.models.addField(mod, mw.col.models.newField(get_plugin().config.note_question))
            mw.col.models.addField(mod, mw.col.models.newField(get_plugin().config.note_answer))
            mw.col.models.addField(mod, mw.col.models.newField(get_plugin().config.note_info))
            # simple template for the model
            tmp = mw.col.models.newTemplate(get_plugin().config.template)
            if get_plugin().config.type_answer:
                tmp['qfmt'] = '{{'+get_plugin().config.note_question+'}}<hr/>{{type:'+get_plugin().config.note_answer+'}}'
                tmp['afmt'] = '{{FrontSide}}<hr/>{{'+get_plugin().config.note_info+'}}'
            else:
                tmp['qfmt'] = '{{'+get_plugin().config.note_question+'}}'
                tmp['afmt'] = '{{FrontSide}}<hr/>{{'+get_plugin().config.note_answer+'}}<hr/>{{'+get_plugin().config.note_info+'}}'
            mw.col.models.addTemplate(mod, tmp)
            # [TODO] Maby should I here move deck selecting?
            mw.col.models.add(mod)
        mw.col.models.setCurrent(mod)

    def add_note(self, q, a, e = ''):
        # adds card to collection
        self.setup()

        note = self.get_note(q)
        if note != None:
            if not a in [s.strip() for s in note[get_plugin().config.note_answer].split(';')]:
                note[get_plugin().config.note_answer] += '; ' + a
                note[get_plugin().config.note_info] += '; ' + e
                note.flush()
        else:
            note = mw.col.newNote()
            note[get_plugin().config.note_question] = q
            note[get_plugin().config.note_answer] = a
            note[get_plugin().config.note_info] = e
            mw.col.addNote(note)
            mw.reset()

    def add_tag(self, q, t):
        # adds tag to note
        self.setup()

        note = self.get_note(q)
        if not note: raise "Najpierw otaguj siebie, zanim zaczniesz tagować to co nie istnieje..."
        note.tags.append(t)
        note.flush()
        mw.reset()

    def get_note(self, q):
        # returns card with selected question
        self.setup()

        notes = mw.col.findNotes('"'+re.escape(q)+'"')
        for note in [mw.col.getNote(n) for n in notes]:
            if note[get_plugin().config.note_question] == q: return note
        return None

    def is_note(self, q, a):
        # checks if <question, answer> is in collection

        note = self.get_note(q)
        if not note: return False
        answers = [s.strip() for s in note[get_plugin().config.note_answer].split(';')]
        if a in answers: return True
        return False
