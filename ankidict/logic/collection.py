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

from addon.main import get_plugin

class Collection(object):
    """Interface functions: get_deck_names, add_note. The rest is for internal
    use, 'private'.
    """
    def select_deck(self, deckname):
        """Select deck for adding cards.
        Select deck with given name so that anki functions will add to
        this deck. Also select note model defined in config. Called from
        add_note(...) method.
        """
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
            mw.col.models.add(mod)
        mw.col.models.setCurrent(mod)

    def add_note(self, q, a, deckname, e = ''):
        # adds card to collection
        self.select_deck(deckname)

        note = self.get_note_by_question(q)
        if note != None:
            # do nothing since it is already in the collection...
            # TODO: some special handling of groups of synonyms
            #       but it needs also special card type for them
            pass
        else:
            note = mw.col.newNote()
            note[get_plugin().config.note_question] = q
            note[get_plugin().config.note_answer] = a
            note[get_plugin().config.note_info] = e
            mw.col.addNote(note)
            mw.reset()

    def get_note_by_question(self, q):
        """Return card with question being exactly q or None."""
        #DANGER: needs select_deck called before!

        notes = mw.col.findNotes('"'+re.escape(q)+'"')
        for note in [mw.col.getNote(n) for n in notes]:
            if note[get_plugin().config.note_question] == q: return note
        return None

    def get_deck_names(self):
        return mw.col.decks.allNames()
